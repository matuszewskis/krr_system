from io import StringIO
import sys
import streamlit as st
from krr_system import (
    TimeDomainDescription,
    Fluent,
    Scenario,
)


# to be deleted when TimeDomainDescription.description() will return value instead of print
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


file_fluents = open("variables/fluents.txt", "r")
list_of_fluents = file_fluents.read()

file_actions = open("variables/actions.txt", "r")
list_of_actions = file_actions.read()

file_durations = open("variables/durations.txt", "r")
list_of_durations = file_durations.read()

file_statements = open("variables/statements.txt", "r")
list_of_statements = file_statements.read()

file_initial_states = open("variables/initial_states.txt", "r")
list_of_initial_states = file_initial_states.read()

file_observations = open("variables/observations.txt", "r")
list_of_observations = file_observations.read()

file_action_occurences = open("variables/action_occurences.txt", "r")
list_of_action_occurences = file_action_occurences.read()


st.title("Knowledge Representation and Reasoning")

st.header("Project D: Actions with Duration")

reset_button = st.button(label="Reset environment")

st.header("Domain Description")
if reset_button:
    list_of_fluents = ""
    list_of_actions = ""
    list_of_durations = ""
    list_of_statements = ""
    list_of_initial_states = ""
    list_of_observations = ""
    list_of_action_occurences = ""
    file_fluents = open("variables/fluents.txt", "w")
    file_actions = open("variables/actions.txt", "w")
    file_durations = open("variables/durations.txt", "w")
    file_statements = open("variables/statements.txt", "w")
    file_initial_states = open("variables/initial_states.txt", "w")
    file_observations = open("variables/observations.txt", "w")
    file_action_occurences = open("variables/action_occurences.txt", "w")
    file_fluents.write("")
    file_actions.write("")
    file_durations.write("")
    file_statements.write("")
    file_initial_states.write("")
    file_observations.write("")
    file_action_occurences.write("")


# fluents & actions input

col1, col2 = st.columns([5, 1])

with col1:
    fluent_input = st.text_input(label="Input fluent", max_chars=100)
    action_input = st.text_input(label="Input action", max_chars=100)

with col2:
    st.text("")
    fluent_button = st.button(label="Submit fluent")
    st.text("")
    action_button = st.button(label="Submit action")


if fluent_button:
    file_fluents = open("variables/fluents.txt", "a")

    if len(list_of_fluents) == 0:
        file_fluents.write(fluent_input)
    else:
        file_fluents.write("," + fluent_input)
        list_of_fluents += ","

    list_of_fluents += fluent_input

if action_button:
    file_actions = open("variables/actions.txt", "a")

    if len(list_of_actions) == 0:
        file_actions.write(action_input)
    else:
        file_actions.write("," + action_input)
        list_of_actions += ","

    list_of_actions += action_input


# duration input

col1, col2, col3 = st.columns([3, 2, 1])

action_durations = list_of_durations.split(",")
action_values = [action_duration.split(";")[0] for action_duration in action_durations]
durations_to_choose = [
    action for action in list_of_actions.split(",") if action not in action_values
]
st.write(durations_to_choose)

with col1:
    fluent_duration = st.selectbox("Choose action to set duration", durations_to_choose)

with col2:
    duration = st.number_input(label="Set duration", min_value=0, step=1)

with col3:
    duration_button = st.text("")
    if len(durations_to_choose) > 0:
        duration_button = st.button(label="Submit duration")
    else:
        duration_button = st.button(label="Submit duration", disabled=True)

if duration_button:
    duration_couple = f"{fluent_duration};{duration}"

    file_durations = open("variables/durations.txt", "a")

    if len(list_of_durations) == 0:
        file_durations.write(duration_couple)
    else:
        file_durations.write("," + duration_couple)
        list_of_durations += ","

    list_of_durations += duration_couple


# statement input

st.subheader("Statements")
col1, col2, col3, col4 = st.columns([3, 3, 2, 1])


with col1:
    statement_action = st.selectbox("Choose action", list_of_actions.split(","))
    statement_type = st.selectbox(
        "Choose type of statement", ["causes", "releases", "impossible"]
    )
with col2:
    if statement_type != "impossible":
        statement_fluent = st.selectbox("Choose fluent", list_of_fluents.split(","))
        statement_fluent_state = st.selectbox("Choose fluent state", [True, False])
        statement_fluent_button = st.button(label="Add new fluent")

with col3:
    statement_condition = st.selectbox("Choose condition", list_of_fluents.split(","))
    statement_condition_state = st.selectbox("Choose condition state", [True, False])
with col4:
    duration_button = st.text("")
    duration_button = st.button(label="Submit statement")

if duration_button:
    if (statement_type != "releases") and (statement_type != "impossible"):
        statement_quartet = f"{statement_action};{statement_type};{statement_fluent};{statement_fluent_state};{statement_condition};{statement_condition_state}"
    elif statement_type != "releases":
        statement_quartet = f"{statement_action};{statement_type};;;{statement_condition};{statement_condition_state}"
    else:
        statement_quartet = f"{statement_action};{statement_type};{statement_fluent};{statement_fluent_state};;;"

    file_statements = open("variables/statements.txt", "a")

    if len(list_of_statements) == 0:
        file_statements.write(statement_quartet)
    else:
        file_statements.write("," + statement_quartet)
        list_of_statements += ","

    list_of_statements += statement_quartet

    st.write(f"{statement_quartet}")
    st.write(list_of_statements.split(","))


# initial condition input

st.subheader("Initial condition")
col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    initial_state_fluent = st.selectbox(
        key="initial_state_fluent",
        label="Choose fluent",
        options=list_of_fluents.split(","),
    )
with col2:
    initial_state_fluent_value = st.selectbox(
        key="initial_state_fluent_value",
        label="Choose fluent state",
        options=[True, False],
    )
with col3:
    st.write("")
    initial_state = st.button(label="Submit inital state")

if initial_state:
    initial_state_couple = f"{initial_state_fluent};{initial_state_fluent_value}"

    file_initial_states = open("variables/initial_states.txt", "a")

    if len(list_of_initial_states) == 0:
        file_initial_states.write(initial_state_couple)
    else:
        file_initial_states.write("," + initial_state_couple)
        list_of_initial_states += ","

    list_of_initial_states += initial_state_couple


st.header("Scenario")


# observations input

st.subheader("Observations")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    observation_fluent = st.selectbox(
        key="observation_fluent",
        label="Choose fluent",
        options=list_of_fluents.split(","),
    )
with col2:
    observation_fluent_value = st.selectbox(
        key="observation_fluent_value",
        label="Choose fluent state",
        options=[True, False],
    )
with col3:
    st.write("")
    observation = st.button(label="Submit observation")

if observation:
    observation_couple = f"{observation_fluent};{observation_fluent_value}"

    file_observations = open("variables/observations.txt", "a")

    if len(list_of_observations) == 0:
        file_observations.write(observation_couple)
    else:
        file_observations.write("," + observation_couple)
        list_of_observations += ","

    list_of_observations += observation_couple


# action occurences input

st.subheader("Action occurences")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    action_occurence = st.selectbox(
        key="action_occurence",
        label="Choose action occurence",
        options=list_of_actions.split(","),
    )
with col2:
    action_occurence_time = st.number_input(
        key="action_occurence_time", label="Choose occurence time", min_value=0
    )
with col3:
    st.write("")
    action_occurence_button = st.button(label="Submit action occurence")

if action_occurence_button:
    action_occurence_couple = f"{action_occurence};{action_occurence_time}"

    file_action_occurences = open("variables/action_occurences.txt", "a")

    if len(list_of_action_occurences) == 0:
        file_action_occurences.write(action_occurence_couple)
    else:
        file_action_occurences.write("," + action_occurence_couple)
        list_of_action_occurences += ","

    list_of_action_occurences += action_occurence_couple


# model preparation

calculate_button = st.button("Calculate model")

if calculate_button:
    m = TimeDomainDescription()
    for initial_state in list_of_initial_states.split(","):
        state = initial_state.split(";")
        m.initially(**{state[0]: bool(state[1])})

    for duration in list_of_durations.split(","):
        state = duration.split(";")
        m.duration(state[0], int(state[1]))
    for statement in list_of_statements.split(","):
        stmnt = statement.split(";")
        if stmnt[1] == "causes":
            m.causes(
                stmnt[0],
                Fluent(**{stmnt[2]: bool(stmnt[3])}),
                conditions=Fluent(**{stmnt[4]: bool(stmnt[5])}),
            )
        elif stmnt[1] == "releases":
            m.releases(stmnt[0], Fluent(**{stmnt[2]: bool(stmnt[3])}))
    #         if stmnt[1] == 'impossible':
    #             m.impossible(stmnt[0], conditions=Fluent(**{stmnt[4]: bool(stmnt[5])}))

    OBS_list = []
    for observation in list_of_observations.split(","):
        obs = observation.split(";")
        OBS_list.append(Fluent(**{obs[0]: bool(obs[1])}))
    OBS = (OBS_list, 1)

    ACS_list = []
    for action in list_of_action_occurences.split(","):
        acs = action.split(";")
        ACS_list.append((acs[0], int(acs[1])))
    ACS = tuple(ACS_list)

    with Capturing() as output:
        m.description()
    st.write(output)

    s = Scenario(domain=m, observations=OBS, action_occurances=ACS)

    try:
        with Capturing() as output:
            s_result = s.is_consistent(verbose=True)
        st.write(output)
        st.write(f"Is consistnet: {s_result}")
    except Exception as e:
        st.write(f"Your mistake: {e}")


# sidebar with current values

with st.sidebar:
    st.subheader("Current example")
    if len(list_of_fluents) == 0:
        st.text("--- no fluents inserted ---")
    else:
        st.text("Fluents")
        for fluent in list_of_fluents.split(","):
            st.text("- " + fluent)
    if len(list_of_actions) == 0:
        st.text("--- no actions inserted ---")
    else:
        try:
            action_durations = list_of_durations.split(",")
            action_values = [
                action_duration.split(";")[0] for action_duration in action_durations
            ]
            action_durations_values = [
                action_duration.split(";")[1] for action_duration in action_durations
            ]
        except:
            pass
        st.text("Actions (duration)")
        for action in list_of_actions.split(","):
            if action in action_values:
                st.text(
                    "- "
                    + action
                    + " ( "
                    + action_durations_values[action_values.index(action)]
                    + " )"
                )
            else:
                st.text("- " + action + "(no duration set)")

    if len(list_of_statements) == 0:
        st.text("--- no statements inserted ---")
    else:
        st.text("Statements")
        for statement in list_of_statements.split(","):
            stmnt = statement.split(";")
            st.text(
                f"ACTION {stmnt[0]} {stmnt[1]} FLUENT {stmnt[2]}={stmnt[3]} GIVEN THAT {stmnt[4]}={stmnt[5]}"
            )
    action_durations = list_of_durations.split(",")

    if len(list_of_initial_states) == 0:
        st.text("--- no initial values inserted ---")
    else:
        st.text("Initial state")
        for initial_state in list_of_initial_states.split(","):
            state = initial_state.split(";")
            st.text(f"- {state[0]}={state[1]}")

    if len(list_of_observations) == 0:
        st.text("--- no observations inserted ---")
    else:
        st.text("Observations")
        for observation in list_of_observations.split(","):
            obs = observation.split(";")
            st.text(f"- {obs[0]}={obs[1]}")

    if len(list_of_action_occurences) == 0:
        st.text("--- no action occurences inserted ---")
    else:
        st.text("Action occurences")
        for action_occurence in list_of_action_occurences.split(","):
            act = action_occurence.split(";")
            st.text(f"- {act[0]}={act[1]}")
