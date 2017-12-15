
import re
import json
import requests

from config import Config

from multiprocessing.connection import Client


class world_object:
    def __init__(self, shared_status, actuators):
        self.shared_status = shared_status
        self.actuators = actuators
        self.time_clock = None
        self.initialize()

    def addTimeClock(self, time_clock):
        self.time_clock = time_clock


class actuators:
    def __init__(self, connection_data):
        self.connection_data = connection_data

    def send_to_sender(self, msg):
        address = ('127.0.0.1', 6000)
        with Client(address, family='AF_INET', authkey=b'secret password') as conn:
            conn.send(msg)

    def output_text(self, who, text):
        send_text = ""
        if who.my_name == "":
            send_text = "<i>{}</i>".format(text)
        else:
            send_text = "<b>{}</b>: {}".format(who.my_name, text)
        msg = {
            "chat_id": self.connection_data["chat_id"],
            "message": send_text,
            "type": "text"
        }
        self.send_to_sender(msg)

    def output_photo(self, who, url):
        msg = {
            "chat_id": self.connection_data["chat_id"],
            "message": url,
            "type": "photo"
        }
        self.send_to_sender(msg)


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
            "question_classification_b": False,
            "question_planning_a": False
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
            if user_entities is not None:
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
                if entity < 0.1 or entity > 0.9:
                    self.actuators.output_text(self, "Creo que tiene que ser un valor entre 0.1 y 0.9")
                    if entity < 0.1:
                        entity = 0.1
                    elif entity > 0.9:
                        entity = 0.9
                if entity == 0.1:
                    img_url = "https://imgur.com/download/6GsPooe"
                elif entity == 0.2:
                    img_url = "https://imgur.com/download/as4EFkT"
                elif entity == 0.3:
                    img_url = "https://imgur.com/download/VNAOhMI"
                elif entity == 0.4:
                    img_url = "https://imgur.com/download/EN0ILDU"
                elif entity == 0.5:
                    img_url = "https://imgur.com/download/WTFBYMG"
                elif entity == 0.6:
                    img_url = "https://imgur.com/download/ADvh0mh"
                elif entity == 0.7:
                    img_url = "https://imgur.com/download/aVL4Wqv"
                elif entity == 0.8:
                    img_url = "https://imgur.com/download/lCyvPks"
                elif entity == 0.9:
                    img_url = "https://imgur.com/download/lE0BdJN"
                self.actuators.output_photo(self, img_url)
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
        if self.status["question_planning_a"]:
            if user_entities is not None:
                answer_ok = True
                answer = [1, 4, 6, 8]
                if len(answer) != len(user_entities):
                    answer_ok = False
                else:
                    for n in range(len(user_entities)):
                        if user_entities[n] != answer[n]:
                            answer_ok = False
                if answer_ok:
                    self.actuators.output_text(self, "¡Excelente!")
                    self.status["question_planning_a"] = False
                    return
                else:
                    if len(user_entities) > len(answer):
                        self.actuators.output_text(self, "El robot dió algunas vueltas de más. Probemos de nuevo.")
                    else:
                        self.actuators.output_text(self, "Debe haber un mejor camino...")
                    narrator.status["time"] -= 1
                    return
            if user_input in ["pass", "i_want_to_know"]:
                self.actuators.output_text(self, "Voy a probar seleccionando el camino 1, 2, 3, 7")
                self.actuators.output_text(self, "¡Es el mas corto!")
                self.status["question_planning_a"] = False
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

        # globo ocular
        # hardware
        # Inteligencia
        # Inteligencia Artificial
        # IA
        # Regla de Bayes
        # Astronauta
        # pizarra
        # digital
        # clasificar
        # pendiente
        # Red Neuronal
        # neurona
        # Aprendizaje Supervisado


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
            self.actuators.output_photo(self, "https://imgur.com/download/65pQaLY")
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
            return
        elif self.status["time"] == 3:
            self.actuators.output_text(self, "rDany se levanta y saluda sonriente.")
            self.actuators.output_photo(self, "https://imgur.com/download/7KRbmcK")
            self.actuators.output_text(rdany_actor, "¡Acá estoy! Perdón la demora, sufrí un pequeño accidente.")
            rdany_actor.status["flatfall"] = False
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 4:
            self.actuators.output_text(self, "No logras contener la risa, la imagen parece salida de una película de zombies robóticos.")
            self.actuators.output_text(self, "rDany larga una carcajada mientras ajusta su globo ocular nuevamente en su lugar.")
            rdany_actor.status["disonnected_eye"] = False
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 5:
            # Pause
            # self.time_clock.get_user_input()
            # return
            pass
        elif self.status["time"] == 6:
            if not rdany_actor.status["say_i_am_doing_a_robot"]:
                self.actuators.output_text(rdany_actor, "Empecemos a trabajar!")
            if not rdany_actor.status["grabbing_robot"]:
                self.actuators.output_text(self, "rDany levanta un pequeño robot del suelo.")
            self.actuators.output_photo(self, "https://imgur.com/download/0yf5DE9")
            self.actuators.output_text(rdany_actor, "Ya completé el hardware, le puse seis ruedas para que pueda manejarse bien en la superficie Marciana.")
            self.actuators.output_text(rdany_actor, "También le agregué varios sensores. Solo estaría faltando cargarle la Inteligencia Artificial.")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 7:
            self.actuators.output_text(rdany_actor, "Necesitamos completar el trabajo para sumar puntos.")
            self.actuators.output_text(rdany_actor, "No podemos fallar. De otra manera no podremos entrar a la academia de Astronautas")
            self.actuators.output_text(self, "rDany toma una pizarra digital y escribe tres puntos:\n- Enseñarle a decidir a que velocidad ir\n- Enseñarle a clasificar rocas\n- Enseñarle a encontrar el camino mas corto")
            # self.actuators.output_text(self, "")
            # self.actuators.output_text(self, "")
            # self.actuators.output_text(self, "")
            self.actuators.output_text(rdany_actor, "El robot tiene que poder hacer estas tres cosas.")
            self.actuators.output_text(rdany_actor, "Comencemos por enseñarle a que velocidad ir, dependiendo de que tan suave sea el terreno.")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 8:
            self.actuators.output_photo(self, "https://imgur.com/download/u3TPGT6")
            self.actuators.output_text(rdany_actor, "Verifiqué que si el terreno tiene una suavidad de 1 el robot podrá ir a 0,5 km/h")
            self.actuators.output_text(rdany_actor, "Y si tiene una suavidad de 10 podrá ir a máxima velocidad, 5km/h.")
            self.actuators.output_text(rdany_actor, "¿Pero como hago que deduzca a cuanto ir si la suavidad es 3, o 7?")
        elif self.status["time"] == 9:
            rdany_actor.status["question_regression"] = True
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 10:
            self.actuators.output_photo(rdany_actor, "https://imgur.com/download/6GsPooe")
            self.actuators.output_text(rdany_actor, "Ahí agregué una línea, solo faltaría ajustarla. El valor de la pendiente 0,1 parece no ser correcto.")
            self.actuators.output_text(rdany_actor, "Probemos otro valor ¿Cual se te ocurre que puede ser?")
        elif self.status["time"] == 11:
            rdany_actor.status["question_regression_b"] = True
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 12:
            self.actuators.output_photo(self, "https://imgur.com/download/6U8QNvm")
            self.actuators.output_text(rdany_actor, "Ahora nuestro robot sabrá a que velocidad ir, no importa cual sea el valor de suavidad")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 13:
            self.actuators.output_text(rdany_actor, "Solo falta enseñarle dos cosas:\n- A clasificar rocas\n- A encontrar el camino mas corto")
            # self.actuators.output_text(rdany_actor, "")
            # self.actuators.output_text(rdany_actor, "")
            self.actuators.output_text(rdany_actor, "Para clasificar rocas estuve preparando una Red Neuronal, que a partir de Aprendizaje Supervisado aprenda a distinguir las rocas que queremos recolectar de las que no.")
            # self.actuators.output_text(rdany_actor, "")
            self.actuators.output_text(rdany_actor, "Aquí hay algunos ejemplos:")
            self.actuators.output_photo(self, "https://imgur.com/download/HZA4Mhd")
            self.actuators.output_text(rdany_actor, "Sin embargo con solo estos ejemplos apenas pude hacer que elija correctamente 5 de cada 10 rocas.")
            self.actuators.output_text(rdany_actor, "Deberás ayudarme a enseñarle nuevos ejemplos para que disminuya el error:")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 14:
            self.actuators.output_text(self, "rDany toma varias rocas de una caja y te las muestra:")
            self.actuators.output_photo(self, "https://imgur.com/download/Sw6ybyd")
            self.actuators.output_text(self, "¿Cuales SI deben analizarse?")
            rdany_actor.status["question_classification_a"] = True
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 15:
            self.actuators.output_text(self, "¿Y cuales NO deben analizarse?")
            rdany_actor.status["question_classification_b"] = True
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 16:
            self.actuators.output_text(self, "rDany carga los nuevos datos en la IA del robot, que ahora elije correctamente 9 de cada 10 rocas.")
            self.actuators.output_text(rdany_actor, "¡Mucho mejor! Sería ideal que elija correctamente todas las rocas, pero como bien sabemos la Regla de Bayes no lo permite.")
            self.actuators.output_text(rdany_actor, "No todos los problemas tienen soluciones perfectas.")
            self.actuators.output_text(rdany_actor, "Ahora solo pasa enseñarle una sola cosa:\n- A encontrar el camino mas corto")
            # self.actuators.output_text(rdany_actor, "")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 17:
            self.actuators.output_photo(rdany_actor, "https://imgur.com/download/qCG1vVl")
            self.actuators.output_text(rdany_actor, "Éste es un mapa de ejemplo")
            self.actuators.output_text(rdany_actor, "¿Si el robot está en el punto verde, cual será la secuencia de posiciones ABCDE que hará que recorra el menor camino hasta la roca situada en el punto azul?")
            self.actuators.output_text(rdany_actor, "El largo de cada camino está marcado en rojo.")
            rdany_actor.status["question_planning_a"] = True
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 18:
            self.actuators.output_text(self, "rDany salta de alegría")
            self.actuators.output_text(rdany_actor, "Ahora es tiempo de probar la IA que armamos en el robot.")
            self.actuators.output_text(rdany_actor, "Estoy tan nerviosa, realmente quiero ser Astronauta ¿Te imaginás?")
            self.actuators.output_text(rdany_actor, "rDany pone voz seria y alza las manos enfatizando")
            self.actuators.output_text(self, "“rDany, la primera astronauta robot”")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 19:
            self.actuators.output_text(self, "Mientras se ríe nerviosamente la IA termina de cargar en el pequeño robot, y rDany lo enciende.")
            self.actuators.output_text(self, "El robot utiliza su cámara para escanear el ambiente, ve una roca, pero la Red Neuronal indica que no es interesante.")
            self.actuators.output_text(self, "Unos metros mas adelante hay otra roca, ésta vez la Red Neuronal clasifica la roca como “interesante”, sin embargo está muy lejos, y hay varios obstáculos en el camino.")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 20:
            self.actuators.output_text(self, "El robot genera un plan con diferentes caminos posibles, pero rápidamente elije el mas corto, lo cual le permitirá ahorrar energía.")
            self.actuators.output_text(self, "Mientras avanza va censando el terreno, y verifica que el suelo del laboratorio es muy suave, nivel 9, así que decide avanzar a 4,5 km/h.")
            self.actuators.output_text(rdany_actor, "¡Lo logramos! Choca los cinco")
            self.actuators.output_text(self, "rDany acerca la mano a la pantalla de la notebook.")
            self.time_clock.get_user_input()
            return
        elif self.status["time"] == 21:
            self.actuators.output_text(rdany_actor, "Estoy segura que con este proyecto nos dejarán entrar en la academia de Astronautas. No veo la hora de estar en el espacio, flotando.")
            self.actuators.output_text(self, "rDany se sienta en el suelo y comienza a desparramar piedras por todo el laboratorio mientras el robot las recolecta.")
            # self.actuators.output_text(self, "FIN")
            self.time_clock.get_user_input()
            return


class time_clock:
    def __init__(self, shared_status, actors, connection_data):
        self.shared_status = shared_status
        self.actors = actors
        self.connection_data = connection_data
        self.read_user_input = True

    def tick(self):
        for actor in self.actors:
            actor["object"].tick()
        # self.shared_status["user_input"] = None

    def get_actor(self, actor_name):
        for actor in self.actors:
            if actor["name"] == actor_name:
                return actor["object"]

    def get_user_input(self):
        self.read_user_input = True

    def set_user_input(self, input_text):
        self.read_user_input = False
        self.connection_data["chat_id"] = input_text["chat_id"]
        self.shared_status["user_entities"] = None
        self.shared_status["user_input"] = None
        if input_text["input_text"] is None:
            return
        entities = []
        reg = re.compile(r'(\s|^|\W)(?P<number>\d\.*\d*|\.\d+)')
        m = reg.finditer(input_text["input_text"])
        entity_number = None
        for match in m:
            entities.append(float(match.group('number')))
        if len(entities) > 0:
            self.shared_status["user_entities"] = entities
        #
        if len(entities) == 0:
            input_obj = {'text': input_text["input_text"]}
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
connection_data = {
    "chat_id": None
}
Actuators = actuators(connection_data)
rDany = rdany(shared_status, Actuators)
Notebook = notebook(shared_status, Actuators)
Narrator = narrator(shared_status, Actuators)
objects = [
    {"name": "rDany", "object": rDany},
    {"name": "Notebook", "object": Notebook},
    {"name": "Narrator", "object": Narrator}
]
TimeClock = time_clock(shared_status, objects, connection_data)

rDany.addTimeClock(TimeClock)
Narrator.addTimeClock(TimeClock)

print()
address = ('127.0.0.1', 6001)
while 1:
    if TimeClock.read_user_input:
        input_text = None
        while input_text is None:
            with Client(address, authkey=b'secret password') as conn:
                    input_text = conn.recv()
                    if input_text is not None:
                        print(input_text)
                        TimeClock.set_user_input(input_text)
    TimeClock.tick()
    Narrator.status["time"] += 1
