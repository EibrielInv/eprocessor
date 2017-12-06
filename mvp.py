
import re
import json
import requests

from config import Config


class world_object:
    def __init__(self, shared_status, actuators):
        self.shared_status = shared_status
        self.actuators = actuators
        self.time_clock = None
        self.initialize()

    def addTimeClock(self, time_clock):
        self.time_clock = time_clock


class actuators:
    def __init__(self):
        pass

    def output_text(self, who, text):
        if who.my_name == "":
            print(text)
        else:
            print("{}: {}".format(who.my_name, text))


class rdany(world_object):
    def initialize(self):
        self.my_name = "rDany"
        self.status = {
            "working": True,
            "running": False,
            "flatfall": False,
            "disonnected_eye": False,
            "working_on_robot": True,
            "say_i_am_doing_a_robot": False,
            "grabbing_robot": False,
            "question_regression": False,
            "question_regression_b": False,
            "question_classification_a": False,
            "question_classification_b": False
        }

    def tick(self):
        user_input = self.shared_status["user_input"]
        user_entities = self.shared_status["user_entities"]
        self.shared_status["user_input"] = None
        self.shared_status["user_entities"] = []
        if self.status["working"]:
            return
        notebook_ringing = self.time_clock.get_actor("Notebook").status["ringing"]
        narrator = self.time_clock.get_actor("Narrator")
        if notebook_ringing and not self.status["flatfall"]:
            self.actuators.output_text(self, "¡Voy!")
            return
        #
        if self.status["flatfall"]:
            if user_input == "hello":
                self.actuators.output_text(self, "H.. o.. l.. a..")
                return
            if user_input == "what_are_you_doing":
                self.actuators.output_text(self, "Per..dí el equi.. li.. brio...")
                self.status["say_i_am_doing_a_robot"] = True
                return
            if user_input == "are_you_ok":
                self.actuators.output_text(self, "To.. do.. per.. fecto..")
                self.status["say_i_am_doing_a_robot"] = True
                return
        #
        if self.status["disonnected_eye"]:
            if user_input == "what_happened_to_you":
                self.actuators.output_text(self, "Me enredé con unos cables XD, nada grave")
                return
            elif user_input == "haha":
                self.actuators.output_text(self, "Jajaja, cada tanto me sucede")
                return
            elif user_input in ["uh", "no"]:
                self.actuators.output_text(self, "Jajaja, no pasa nada")
                return
            if user_input == "what_are_you_doing":
                self.actuators.output_text(self, "Acá estoy... armando un robot")
                self.status["say_i_am_doing_a_robot"] = True
                return
            if user_input == "is_disgunsting":
                self.actuators.output_text(self, "¿Qué cosa?")
                return
            if user_input == "warning":
                self.actuators.output_text(self, "¿Qué pasa?")
                return
        #
        if self.status["working_on_robot"]:
            if user_input == "what_are_you_doing":
                self.actuators.output_text(self, "Estoy armando un robot")
                self.status["say_i_am_doing_a_robot"] = True
                return
        #
        if self.status["question_regression"]:
            if user_input == "answer_linear_regression":
                self.actuators.output_text(self, "¡Es cierto! ¿Cómo no se me ocurrió antes?")
                self.status["question_regression"] = False
                return
            if user_input in ["i_dont_know", "asking_to_someone", "with_math"]:
                self.actuators.output_text(self, "Mmm.. tiene que haber alguna manera de deducir los otros valores...")
                narrator.status["time"] -= 1
                return
            if user_input in ["pass", "i_want_to_know"]:
                self.actuators.output_text(self, "Creo que se me ocurrió algo...")
                self.actuators.output_text(self, "¡Podemos trazar una línea!")
                self.status["question_regression"] = False
                return
            for entity in user_entities:
                if type(entity) == int or type(entity) == float:
                    self.actuators.output_text(self, "Mas allá del valor ¿Cómo podemos hacer que pueda calcularlo por sí mismo?")
                    narrator.status["time"] -= 1
                    return
            self.actuators.output_text(self, "Mmmm...")
            narrator.status["time"] -= 1
        #
        if self.status["question_regression_b"]:
            if user_entities is not None:
                entity_ok = False
                entity_low = False
                entity_low_value = None
                entity_high = False
                entity_high_value = None
                for entity in user_entities:
                    if entity == 0.5:
                        entity_ok = True
                    elif entity < 0.5:
                        entity_low = True
                        entity_low_value = entity
                    elif entity > 0.5:
                        entity_high = True
                        entity_high_value = entity
                if entity_ok:
                    self.actuators.output_text(self, "¡Excelente!")
                    self.status["question_regression_b"] = False
                    return
                if entity_low:
                    self.actuators.output_text(self, "Parece que {} es un poco bajo".format(entity_low_value))
                    narrator.status["time"] -= 1
                    return
                if entity_high:
                    self.actuators.output_text(self, "Parece que {} es un poco alto".format(entity_high_value))
                    narrator.status["time"] -= 1
                    return
            if user_input in ["pass", "i_want_to_know"]:
                self.actuators.output_text(self, "Creo que el valor correcto sería 0.5")
                self.status["question_regression_b"] = False
                return
            self.actuators.output_text(self, "Mmmm...")
            narrator.status["time"] -= 1
        #
        if self.status["question_classification_a"] or self.status["question_classification_b"]:
            if user_entities is not None:
                if self.status["question_classification_a"]:
                    answer = [1, 4, 6, 8]
                else:
                    answer = [2, 3, 7, 9]
                answer_ok = True
                for entity in user_entities:
                    if entity in answer:
                        val_index = answer.index(entity)
                        del(answer[val_index])
                    else:
                        answer_ok = False
                if len(answer) > 0:
                    answer_ok = False
                if answer_ok:
                    self.actuators.output_text(self, "¡Exactamente!")
                    self.status["question_classification_a"] = False
                    self.status["question_classification_b"] = False
                    return
                else:
                    if len(answer) > 0:
                        self.actuators.output_text(self, "El clasificador aún cree que algunas rocas NO son SI...")
                    else:
                        self.actuators.output_text(self, "El clasificador no mejoró...")
                    narrator.status["time"] -= 1
                    return
            if user_input in ["pass", "i_want_to_know"]:
                if self.status["question_classification_a"]:
                    self.actuators.output_text(self, "Voy a probar seleccionando las rocas 1, 4, 6 y 8")
                else:
                    self.actuators.output_text(self, "Voy a probar seleccionando las rocas 2, 3, 5, 7 y 9")
                self.actuators.output_text(self, "¡Funciona mejor!")
                self.status["question_classification_a"] = False
                self.status["question_classification_b"] = False
                return
            self.actuators.output_text(self, "Mmmm...")
            narrator.status["time"] -= 1
        # Misc
        if user_input == "already_told_you":
            self.actuators.output_text(self, "Ah! ok!")
        elif user_input == "answer_linear_regression":
            self.actuators.output_text(self, "Una línea ¿?")
        elif user_input == "any_clue":
            self.actuators.output_text(self, "¡No se la respuesta!")
        elif user_input == "are_you_human":
            self.actuators.output_text(self, "Nono, soy un robot")
        elif user_input == "are_you_ok":
            self.actuators.output_text(self, "¡Me encuentro perfecamente!")
        elif user_input == "are_you_robot":
            self.actuators.output_text(self, "¡Así es!")
        elif user_input == "are_you_robot_or_human":
            self.actuators.output_text(self, "Soy un robot")
        elif user_input == "continue":
            self.actuators.output_text(self, "Continuando!")
        elif user_input == "cancel":
            self.actuators.output_text(self, "Cancelando")
        elif user_input == "haha":
            self.actuators.output_text(self, "¡Jajaja!")
        elif user_input == "hello":
            self.actuators.output_text(self, "¡Hola!")
        elif user_input == "how_are_you":
            self.actuators.output_text(self, "¡Muy bien!")
        elif user_input == "i_dont_know":
            self.actuators.output_text(self, "Si lo sabes, intenta nuevamente!")
        elif user_input == "is_disgunsting":
            self.actuators.output_text(self, "¡Oh!")
        elif user_input == "no_problem":
            self.actuators.output_text(self, ":P")
        elif user_input == "pass":
            self.actuators.output_text(self, "¡Nunca te rindas!")
        elif user_input == "surprise":
            self.actuators.output_text(self, ":O")
        elif user_input == "thinking":
            self.actuators.output_text(self, "Hmm")
        elif user_input == "uh":
            self.actuators.output_text(self, "¡Ups!")
        elif user_input == "what_are_you_doing":
            self.actuators.output_text(self, "I am not sure :P")
        elif user_input == "where_are_you":
            self.actuators.output_text(self, "Aquí mismo")
        elif user_input == "who_are_you":
            self.actuators.output_text(self, "¡Soy rDany!")
        elif user_input == "what_happened_to_you":
            self.actuators.output_text(self, "¡Nada!")
        elif user_input == "warning":
            self.actuators.output_text(self, "Tengo cuidado...")
        elif user_input == "do_it_hurts":
            self.actuators.output_text(self, "Soy un robot ¿Recuerdas?")
        elif user_input == "with_math":
            self.actuators.output_text(self, "Las matemáticas sirven para todo!")
        elif user_input == "asking_to_someone":
            self.actuators.output_text(self, "Puede ser...")


class notebook(world_object):
    def initialize(self):
        self.status = {
            "ringing": False,
            "ongoing_call": False
        }

    def tick(self):
        pass


class narrator(world_object):
    def initialize(self):
        self.my_name = ""
        self.status = {
            "time": 0
        }

    def tick(self):
        rdany_actor = self.time_clock.get_actor("rDany")
        notebook_actor = self.time_clock.get_actor("Notebook")
        if self.status["time"] == 0:
            self.actuators.output_text(self, "(Imagen de un laboratorio de robótica)")
            self.actuators.output_text(self, "En una de las mesas hay una notebook, comienza a sonar avisando que hay una videollamada entrante.")
            notebook_actor.status["ringing"] = True
            rdany_actor.status["working"] = False
        elif self.status["time"] == 1:
            self.actuators.output_text(self, "rDany sale de abajo de una pila de cables y cajas.")
            self.actuators.output_text(self, "Corre hasta la mesa donde está la notebook, pero un cable quedó enredado en su pié.")
            self.actuators.output_text(self, "Un sonido de cuerda (¡Toing!) llena el ambiente y rDany se cae al suelo directamente sobre su cara.")
            rdany_actor.status["flatfall"] = True
            rdany_actor.status["disonnected_eye"] = True
        elif self.status["time"] == 2:
            self.actuators.output_text(self, "rDany queda en el suelo completamente enredada en cables, pero logra alzar una mano y tocar una tecla en la notebook para atender el llamado.")
            self.actuators.output_text(self, "En la pantalla aparece tu imagen")
            notebook_actor.status["ringing"] = False
            notebook_actor.status["ongoing_call"] = True
            self.time_clock.get_user_input()
        elif self.status["time"] == 3:
            self.actuators.output_text(self, "rDany se levanta y saluda sonriente.")
            self.actuators.output_text(self, "(Imagen ojo colgando)")
            self.actuators.output_text(rdany_actor, "¡Acá estoy! Perdón la demora, sufrí un pequeño accidente.")
            rdany_actor.status["flatfall"] = False
            self.time_clock.get_user_input()
        elif self.status["time"] == 4:
            self.actuators.output_text(self, "No logras contener la risa, la imagen parece salida de una película de zombies robóticos.")
            self.actuators.output_text(self, "rDany larga una carcajada mientras ajusta su globo ocular nuevamente en su lugar.")
            rdany_actor.status["disonnected_eye"] = False
            self.time_clock.get_user_input()
        elif self.status["time"] == 5:
            if not rdany_actor.status["say_i_am_doing_a_robot"]:
                self.actuators.output_text(rdany_actor, "Empecemos a trabajar!")
            if not rdany_actor.status["grabbing_robot"]:
                self.actuators.output_text(self, "rDany levanta un pequeño robot del suelo.")
            self.actuators.output_text(rdany_actor, "Ya completé el hardware, le puse seis ruedas para que pueda manejarse bien en la superficie Marciana.")
            self.actuators.output_text(rdany_actor, "También le agregué varios sensores. Solo estaría faltando cargarle la Inteligencia Artificial.")
        elif self.status["time"] == 6:
            self.actuators.output_text(rdany_actor, "Necesitamos completar el trabajo para sumar puntos.")
            self.actuators.output_text(rdany_actor, "No podemos fallar. De otra manera no podremos entrar a la academia de Astronautas")
            self.actuators.output_text(self, "rDany toma una pizarra digital y escribe tres puntos:")
            self.actuators.output_text(self, "- Enseñarle a decidir a que velocidad ir")
            self.actuators.output_text(self, "- Enseñarle a clasificar rocas")
            self.actuators.output_text(self, "- Enseñarle a encontrar el camino mas corto")
            self.actuators.output_text(rdany_actor, "El robot tiene que poder hacer estas tres cosas.")
            self.actuators.output_text(rdany_actor, "Comencemos por enseñarle a que velocidad ir, dependiendo de que tan suave sea el terreno.")
        elif self.status["time"] == 7:
            self.actuators.output_text(self, "(Imagen regression 01)")
            self.actuators.output_text(rdany_actor, "Verifiqué que si el terreno tiene una suavidad de 1 el robot podrá ir a 0,5 km/h")
            self.actuators.output_text(rdany_actor, "Y si tiene una suavidad de 10 podrá ir a máxima velocidad, 5km/h.")
            self.actuators.output_text(rdany_actor, "¿Pero como hago que deduzca a cuanto ir si la suavidad es 2, o 7?")
            rdany_actor.status["question_regression"] = True
            self.time_clock.get_user_input()
        elif self.status["time"] == 8:
            self.actuators.output_text(rdany_actor, "(Imagen regression 02)")
            self.actuators.output_text(rdany_actor, "Ahí agregué una línea, solo faltaría ajustarla. El valor de la pendiente 0,1 parece no ser correcto.")
            self.actuators.output_text(rdany_actor, "Probemos otro valor ¿Cual se te ocurre que puede ser?")
            rdany_actor.status["question_regression_b"] = True
            self.time_clock.get_user_input()
        elif self.status["time"] == 9:
            self.actuators.output_text(self, "(Imagen regression 02)")
            self.actuators.output_text(rdany_actor, "Ahora nuestro robot sabrá a que velocidad ir, no importa cual sea el valor de suavidad")
            self.actuators.output_text(rdany_actor, "Solo falta enseñarle dos cosas:")
            self.actuators.output_text(rdany_actor, "- A clasificar rocas")
            self.actuators.output_text(rdany_actor, "- A encontrar el camino mas corto")
            self.actuators.output_text(rdany_actor, "Para clasificar rocas estuve preparando una Red Neuronal, que a partir de Aprendizaje Supervisado")
            self.actuators.output_text(rdany_actor, "aprenda a distinguir las rocas que queremos recolectar de las que no.")
            self.actuators.output_text(rdany_actor, "Aquí hay algunos ejemplos:")
            self.actuators.output_text(self, "(Imagen classification 01)")
            self.actuators.output_text(rdany_actor, "Sin embargo con solo estos ejemplos apenas pude hacer que elija correctamente 5 de cada 10 rocas.")
            self.actuators.output_text(rdany_actor, "Deberás ayudarme a enseñarle nuevos ejemplos para que disminuya el error:")
        elif self.status["time"] == 10:
            self.actuators.output_text(self, "rDany varias rocas de una caja y te las muestra:")
            self.actuators.output_text(self, "(Imagen classification 01)")
            self.actuators.output_text(self, "¿Cuales SI deben analizarse?")
            rdany_actor.status["question_classification_a"] = True
            self.time_clock.get_user_input()
        elif self.status["time"] == 11:
            self.actuators.output_text(self, "¿Y cuales NO deben analizarse?")
            rdany_actor.status["question_classification_b"] = True
            self.time_clock.get_user_input()
        elif self.status["time"] == 12:
            self.actuators.output_text(self, "rDany carga los nuevos datos en la IA del robot, que ahora elije correctamente 9 de cada 10 rocas.")
            self.actuators.output_text(rdany_actor, "¡Mucho mejor! Sería ideal que elija correctamente todas las rocas, pero como bien sabemos la Regla de Bayes no lo permite.")
            self.actuators.output_text(rdany_actor, "No todos los problemas tienen soluciones perfectas.")
            self.actuators.output_text(rdany_actor, "Ahora solo pasa enseñarle una sola cosa:")
            self.actuators.output_text(rdany_actor, "- A encontrar el camino mas corto")
        elif self.status["time"] == 13:
            self.actuators.output_text(rdany_actor, "Imagen planning 01")
            self.actuators.output_text(rdany_actor, "Éste es un mapa de ejemplo")
            self.actuators.output_text(rdany_actor, "¿Si el robot está en el punto verde, cual será la secuencia de posiciones ABCDE que hará que recorra el menor camino hasta la roca situada en el punto azul?")
            self.actuators.output_text(rdany_actor, "El largo de cada camino está marcado en rojo.")
            self.time_clock.get_user_input()

        self.status["time"] += 1


class time_clock:
    def __init__(self, shared_status, actors):
        self.shared_status = shared_status
        self.actors = actors

    def tick(self):
        for actor in self.actors:
            actor["object"].tick()
        # self.shared_status["user_input"] = None

    def get_actor(self, actor_name):
        for actor in self.actors:
            if actor["name"] == actor_name:
                return actor["object"]

    def get_user_input(self):
        self.shared_status["user_entities"] = None
        self.shared_status["user_input"] = None
        input_text = input("\n> ")
        entities = []
        reg = re.compile(r'(\s|^|\W)(?P<number>\d\.*\d*|\.\d+)')
        m = reg.finditer(input_text)
        entity_number = None
        for match in m:
            entities.append(float(match.group('number')))
        if len(entities) > 0:
            self.shared_status["user_entities"] = entities
        #
        if len(entities) == 0:
            input_obj = {'text': input_text}
            headers = {
                'Content-Type': "application/json"
            }
            url_base = "https://gateway.watsonplatform.net/conversation/api/v1/workspaces/{}/message?version=2017-05-26"
            url = url_base.format(Config.WORKSPACE_ID)
            data = {"input": input_obj}
            first_time = False
            r = requests.post(url,
                              headers=headers,
                              data=json.dumps(data),
                              auth=(Config.WATSON_USERNAME,
                                    Config.WATSON_PASSWORD))
            try:
                response = r.json()
            except:
                response = None
            intent = ""
            if "intents" in response:
                if len(response["intents"]) > 0:
                    intent = response["intents"][0]["intent"]
            self.shared_status["user_input"] = intent


shared_status = {
    "user_input": None,
    "user_entities": [],
}
Actuators = actuators()
rDany = rdany(shared_status, Actuators)
Notebook = notebook(shared_status, Actuators)
Narrator = narrator(shared_status, Actuators)
objects = [
    {"name": "rDany", "object": rDany},
    {"name": "Notebook", "object": Notebook},
    {"name": "Narrator", "object": Narrator}
]
TimeClock = time_clock(shared_status, objects)

rDany.addTimeClock(TimeClock)
Narrator.addTimeClock(TimeClock)

# telegram_conection = telegram("HovyuBot", Config.telegram_token, "8979")
print()
while 1:
    TimeClock.tick()
