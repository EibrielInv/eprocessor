
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
            "question_regression": False
        }

    def tick(self):
        user_input = self.shared_status["user_input"]
        self.shared_status["user_input"] = None
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
                self.actuators.output_text(self, "Me enredé con unos cables")
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
            if user_input == "i_dont_know":
                self.actuators.output_text(self, "Mmm.. tiene que haber alguna manera de deducir los otros valores...")
                narrator.status["time"] -= 1
                return
            if user_input in ["pass", "i_want_to_know"]:
                self.actuators.output_text(self, "Creo que se me ocurrió algo...")
                self.actuators.output_text(self, "¡Podemos trazar una línea!")
                return
            self.actuators.output_text(self, "Mmmm...")
            narrator.status["time"] -= 1
        # Misc
        if user_input == "already_told_you":
            self.actuators.output_text(self, "Ah! ok!")
        elif user_input == "answer_linear_regression":
            self.actuators.output_text(self, "Una línea ¿?")
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
            self.actuators.output_text(rdany_actor, "¡Acá estoy! Perdón la demora, sufrí un pequeño accidente.")
            self.actuators.output_text(self, "Uno de los ojos electrónicos larga chispas mientras cuelga de su cuenca apenas sostenido por algunos cables.")
            rdany_actor.status["flatfall"] = False
            self.time_clock.get_user_input()
        elif self.status["time"] == 4:
            self.actuators.output_text(self, "No logras sostener la risa, la imagen parece salida de una ridícula película de zombies robóticos.")
            self.actuators.output_text(self, "rDany no tarda en darse cuenta de lo sucedido, y larga una carcajada mientras ajusta su globo ocular nuevamente en su lugar.")
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
            self.actuators.output_text(rdany_actor, "Verifiqué que si el terreno tiene una suavidad de 1 el robot podrá ir a 0,5 km/h")
            self.actuators.output_text(rdany_actor, "Y si tiene una suavidad de 10 podrá ir a máxima velocidad! A 5km/h.")
            self.actuators.output_text(rdany_actor, "¿Pero como hago que deduzca a cuanto ir si la suavidad es 2, o 7?")
            rdany_actor.status["question_regression"] = True
            self.time_clock.get_user_input()
        elif self.status["time"] == 8:
            self.actuators.output_text(rdany_actor, "Ahí agregué una línea, solo faltaría ajustarla. El valor de la pendiente 0,1 parece no ser correcto.")
            self.actuators.output_text(rdany_actor, "Probemos otro valor ¿Cual se te ocurre que puede ser?")

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
        input_text = input("\n> ")
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
