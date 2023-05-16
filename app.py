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

file_statements = open("variables/statements.txt", "r")
list_of_statements = file_statements.read()

file_initial_states = open("variables/initial_states.txt", "r")
list_of_initial_states = file_initial_states.read()

file_observations = open("variables/observations.txt", "r")
list_of_observations = file_observations.read()

file_action_occurences = open("variables/action_occurences.txt", "r")
list_of_action_occurences = file_action_occurences.read()

file_technical_vars = open("variables/technical_variables.txt", "r")
list_of_technical_vars = file_technical_vars.read()

file_fluents.close()
file_actions.close()
file_statements.close()
file_initial_states.close()
file_observations.close()
file_action_occurences.close()
file_technical_vars.close()

st.title("Knowledge Representation and Reasoning")

st.header("Project D: Actions with Duration")

reset_button = st.button(label="Reset environment")

st.header("Domain Description")
if reset_button:
    list_of_fluents = ""
    list_of_actions = ""
    list_of_statements = ""
    list_of_initial_states = ""
    list_of_observations = ""
    list_of_action_occurences = ""
    list_of_technical_vars = "1;1"
    file_fluents = open("variables/fluents.txt", "w")
    file_actions = open("variables/actions.txt", "w")
    file_statements = open("variables/statements.txt", "w")
    file_initial_states = open("variables/initial_states.txt", "w")
    file_observations = open("variables/observations.txt", "w")
    file_action_occurences = open("variables/action_occurences.txt", "w")
    file_technical_vars = open("variables/technical_variables.txt", "w")
    file_fluents.write("")
    file_actions.write("")
    file_statements.write("")
    file_initial_states.write("")
    file_observations.write("")
    file_action_occurences.write("")
    file_technical_vars.write("1;1")
    file_fluents.close()
    file_actions.close()
    file_statements.close()
    file_initial_states.close()
    file_observations.close()
    file_action_occurences.close()
    file_technical_vars.close()

# fluents input

col1, col2 = st.columns([5, 1])

with col1:
    fluent_input = st.text_input(label="Input fluent", max_chars=100)

with col2:
    st.text("")
    fluent_button = st.button(label="Submit fluent")

if fluent_button:
    file_fluents = open("variables/fluents.txt", "a")

    if len(list_of_fluents) == 0:
        file_fluents.write(fluent_input)
        list_of_fluents += fluent_input
    else:
        list_of_fluents_splitted = list_of_fluents.split(",")
        if fluent_input not in list_of_fluents_splitted:
            file_fluents.write("," + fluent_input)
            list_of_fluents += "," + fluent_input

    file_fluents.close()

# actions input

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    action_input = st.text_input(label="Input action", max_chars=100)

with col2:
    duration_input = st.number_input(label="Input duration", min_value=1, step=1)

with col3:
    st.text("")
    action_button = st.button(label="Submit action")

if action_button:
    action_couple = f"{action_input};{duration_input}"

    file_actions = open("variables/actions.txt", "a")

    if len(list_of_actions) == 0:
        file_actions.write(action_couple)
        list_of_actions += action_couple
    else:
        list_of_actions_splitted = list_of_actions.split(",")
        if action_couple not in list_of_actions_splitted:
            file_actions.write("," + action_couple)
            list_of_actions += "," + action_couple

    file_actions.close()

# duration modification

col1, col2, col3 = st.columns([3, 2, 1])

actions = list_of_actions.split(",")
if len(list_of_actions) == 0:
    action_names = []
    action_durations_values = []
else:
    action_names = [action.split(";")[0] for action in actions]
    action_durations_values = [action.split(";")[1] for action in actions]

with col1:
    duration_action = st.selectbox("Choose action to modify duration", action_names)

with col2:
    duration = st.number_input(label="Modify duration", min_value=1, step=1)

with col3:
    duration_button = st.text("")
    if len(action_names) > 0:
        duration_button = st.button(label="Submit duration")
    else:
        duration_button = st.button(label="Submit duration", disabled=True)

if duration_button:
    file_actions = open("variables/actions.txt", "w")

    action_index = action_names.index(duration_action)
    action_durations_values[action_index] = str(duration)
    new_durations = [
        f"{action_names[i]};{action_durations_values[i]}"
        for i in range(len(action_names))
    ]
    list_of_actions = ",".join(new_durations)
    file_actions.write(list_of_actions)
    file_actions.close()

# statement input

condition_values, fluent_values = list_of_technical_vars.split(";")
condition_values = int(condition_values)
fluent_values = int(fluent_values)

st.subheader("Statements")
col1, col2, col3, col4 = st.columns([4, 3, 3, 2])

with col1:
    statement_action = st.selectbox(
        "Choose action", [action.split(";")[0] for action in list_of_actions.split(",")]
    )
    statement_type = st.radio(
        "Choose type of statement", ("causes", "releases", "impossible")
    )
with col2:
    if statement_type != "impossible":
        statement_fluent_button = st.button(label="Add new fluent")
        statement_fluent_button_remove = st.button(label="Remove fluent")
        if statement_fluent_button:
            if fluent_values > 4:
                st.write("!!! Too many values !!!")
            else:
                fluent_values += 1
        elif statement_fluent_button_remove and fluent_values > 0:
            fluent_values -= 1

        # 1st statement
        if fluent_values > 0:
            statement_fluent_1 = st.selectbox(
                "Choose fluent 1st", list_of_fluents.split(",")
            )
            statement_fluent_false_1 = st.checkbox("False", key="fluent_false_1")
            statement_fluent_state_1 = "False" if statement_fluent_false_1 else "True"

        # 2nd statement
        if fluent_values > 1:
            statement_fluent_2 = st.selectbox(
                "Choose fluent 2nd", list_of_fluents.split(",")
            )
            statement_fluent_false_2 = st.checkbox("False", key="fluent_false_2")
            statement_fluent_state_2 = "False" if statement_fluent_false_2 else "True"

        # 3rd statement
        if fluent_values > 2:
            statement_fluent_3 = st.selectbox(
                "Choose fluent 3rd", list_of_fluents.split(",")
            )
            statement_fluent_false_3 = st.checkbox("False", key="fluent_false_3")
            statement_fluent_state_3 = "False" if statement_fluent_false_3 else "True"

        # 4th statement
        if fluent_values > 3:
            statement_fluent_4 = st.selectbox(
                "Choose fluent 4th", list_of_fluents.split(",")
            )
            statement_fluent_false_4 = st.checkbox("False", key="fluent_false_4")
            statement_fluent_state_4 = "False" if statement_fluent_false_4 else "True"

        # 5th statement
        if fluent_values > 4:
            statement_fluent_5 = st.selectbox(
                "Choose fluent 5th", list_of_fluents.split(",")
            )
            statement_fluent_false_5 = st.checkbox("False", key="fluent_false_5")
            statement_fluent_state_5 = "False" if statement_fluent_false_5 else "True"


with col3:
    statement_condition_button = st.button(label="Add new condition")
    statement_condition_button_remove = st.button(label="Remove condition")
    if statement_condition_button:
        if condition_values > 4:
            st.write("!!! Too many conditions !!!")
        else:
            condition_values += 1
    elif statement_condition_button_remove and condition_values > 0:
        condition_values -= 1

    # 1st statement condition
    if condition_values > 0:
        statement_condition_1 = st.selectbox(
            "Choose condition 1st", list_of_fluents.split(",")
        )
        statement_condition_false_1 = st.checkbox("False", key="condition_false_1")
        statement_condition_state_1 = "False" if statement_condition_false_1 else "True"

    #  2nd statement condition
    if condition_values > 1:
        statement_condition_2 = st.selectbox(
            "Choose condition 2nd", list_of_fluents.split(",")
        )
        statement_condition_false_2 = st.checkbox("False", key="condition_false_2")
        statement_condition_state_2 = "False" if statement_condition_false_2 else "True"

    # 3rd statement condition
    if condition_values > 2:
        statement_condition_3 = st.selectbox(
            "Choose condition 3rd", list_of_fluents.split(",")
        )
        statement_condition_false_3 = st.checkbox("False", key="condition_false_3")
        statement_condition_state_3 = "False" if statement_condition_false_3 else "True"

    # 4th statement condition
    if condition_values > 3:
        statement_condition_4 = st.selectbox(
            "Choose condition 4th", list_of_fluents.split(",")
        )
        statement_condition_false_4 = st.checkbox("False", key="condition_false_4")
        statement_condition_state_4 = "False" if statement_condition_false_4 else "True"

    # 5th statement condition
    if condition_values > 4:
        statement_condition_5 = st.selectbox(
            "Choose condition 5th", list_of_fluents.split(",")
        )
        statement_condition_false_5 = st.checkbox("False", key="condition_false_5")
        statement_condition_state_5 = "False" if statement_condition_false_5 else "True"


with col4:
    submit_button = st.text("")
    submit_button = st.button(label="Submit statement")

file_technical_vars = open("variables/technical_variables.txt", "w")
file_technical_vars.write(f"{condition_values};{fluent_values}")
file_technical_vars.close()

if submit_button:
    statement_conditions = ""
    if condition_values > 0:
        statement_conditions += f"{statement_condition_1}#{statement_condition_state_1}"
    if condition_values > 1:
        statement_conditions += (
            f":{statement_condition_2}#{statement_condition_state_2}"
        )
    if condition_values > 2:
        statement_conditions += (
            f":{statement_condition_3}#{statement_condition_state_3}"
        )
    if condition_values > 3:
        statement_conditions += (
            f":{statement_condition_4}#{statement_condition_state_4}"
        )
    if condition_values > 4:
        statement_conditions += (
            f":{statement_condition_5}#{statement_condition_state_5}"
        )

    if statement_type != "impossible":
        statement_fluents = ""
        if fluent_values > 0:
            statement_fluents += f"{statement_fluent_1}#{statement_fluent_state_1}"
        if fluent_values > 1:
            statement_fluents += f":{statement_fluent_2}#{statement_fluent_state_2}"
        if fluent_values > 2:
            statement_fluents += f":{statement_fluent_3}#{statement_fluent_state_3}"
        if fluent_values > 3:
            statement_fluents += f":{statement_fluent_4}#{statement_fluent_state_4}"
        if fluent_values > 4:
            statement_fluents += f":{statement_fluent_5}#{statement_fluent_state_5}"
        statement_quartet = f"{statement_action};{statement_type};{statement_fluents};{statement_conditions}"
    elif statement_type == "impossible":
        statement_quartet = (
            f"{statement_action};{statement_type};;{statement_conditions}"
        )
    # else:
    #     statement_quartet = f"{statement_action};{statement_type};{statement_fluent};{statement_fluent_state};;;"

    file_statements = open("variables/statements.txt", "a")

    if len(list_of_statements) == 0:
        file_statements.write(statement_quartet)
        list_of_statements += statement_quartet
    else:
        list_of_statements_splitted = list_of_statements.split(",")
        if statement_quartet not in list_of_statements_splitted:
            file_statements.write("," + statement_quartet)
            list_of_statements += "," + statement_quartet
    st.write(list_of_statements)

    file_statements.close()
    st.write(f"{statement_quartet}")
    st.write(list_of_statements.split(","))

# initial condition input

st.subheader("Initial condition")
col1, col2 = st.columns([5, 1])

with col1:
    initial_state_fluent = st.selectbox(
        key="initial_state_fluent",
        label="Choose fluent",
        options=list_of_fluents.split(","),
    )
    initial_state_fluent_false = st.checkbox(
        key="initial_state_fluent_false", label="False"
    )
    initial_state_fluent_value = "False" if initial_state_fluent_false else "True"
with col2:
    st.write("")
    initial_state = st.button(label="Submit inital state")

if initial_state:
    initial_state_couple = f"{initial_state_fluent};{initial_state_fluent_value}"

    file_initial_states = open("variables/initial_states.txt", "a")

    if len(list_of_initial_states) == 0:
        file_initial_states.write(initial_state_couple)
        list_of_initial_states += initial_state_couple
    else:
        list_of_initial_states_splitted = list_of_initial_states.split(",")
        if initial_state_fluent not in [
            initial.split(";")[0] for initial in list_of_initial_states_splitted
        ]:
            file_initial_states.write("," + initial_state_couple)
            list_of_initial_states += "," + initial_state_couple
    file_initial_states.close()

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
    observation_fluent_false = st.checkbox(
        key="observation_fluent_false", label="False"
    )
    observation_fluent_value = "False" if observation_fluent_false else "True"
with col2:
    observation_fluent_time = st.number_input(
        key="observation_fluent_time", label="Choose observation time", min_value=1
    )
with col3:
    st.write("")
    observation = st.button(label="Submit observation")

if observation:
    observation_couple = (
        f"{observation_fluent};{observation_fluent_value};{observation_fluent_time}"
    )

    file_observations = open("variables/observations.txt", "a")

    if len(list_of_observations) == 0:
        file_observations.write(observation_couple)
        list_of_observations += observation_couple
    else:
        list_of_observations_splitted = list_of_observations.split(",")
        existing_observations = [
            [obs.split(";")[0], obs.split(";")[2]]
            for obs in list_of_observations_splitted
        ]
        duplicate_observation = [observation_fluent, str(observation_fluent_time)]
        if duplicate_observation not in existing_observations:
            file_observations.write("," + observation_couple)
            list_of_observations += "," + observation_couple
    file_observations.close()

# action occurences input

st.subheader("Action occurences")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    action_occurence = st.selectbox(
        key="action_occurence",
        label="Choose action occurence",
        options=[action.split(";")[0] for action in list_of_actions.split(",")],
    )
with col2:
    action_occurence_time = st.number_input(
        key="action_occurence_time", label="Choose occurence time", min_value=1
    )
with col3:
    st.write("")
    action_occurence_button = st.button(label="Submit action occurence")

if action_occurence_button:
    action_occurence_couple = f"{action_occurence};{action_occurence_time}"

    file_action_occurences = open("variables/action_occurences.txt", "a")
    st.write()
    if len(list_of_action_occurences) == 0:
        file_action_occurences.write(action_occurence_couple)
        list_of_action_occurences += action_occurence_couple
    else:
        list_of_action_occurence_times = [
            ac.split(";")[1] for ac in list_of_action_occurences.split(",")
        ]
        if action_occurence_time not in list_of_action_occurence_times:
            file_action_occurences.write("," + action_occurence_couple)
            list_of_action_occurences += "," + action_occurence_couple

# action query

st.subheader("Action query")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    action_query = st.selectbox(
        key="action_query",
        label="Choose action",
        options=[action.split(";")[0] for action in list_of_actions.split(",")],
    )
with col2:
    action_query_time = st.number_input(
        key="action_query_time", label="Choose time", min_value=1
    )
with col3:
    st.write("")
    action_query_button = st.button(
        key="action_query_button", label="Calculate action query"
    )

# condition query

st.subheader("Condition query")

col1, col2, col3, col4 = st.columns([3, 4, 3, 2])

with col1:
    condition_query_type = st.selectbox(
        key="condition_query_type",
        label="Choose type",
        options=["necessary", "possible"],
    )
with col2:
    condition_query = st.selectbox(
        key="condition_query",
        label="Choose condition",
        options=list_of_fluents.split(","),
    )
    condition_query_false = st.checkbox(key="condition_query_false", label="False")
    condition_query_value = "False" if condition_query_false else "True"
with col3:
    condition_query_time = st.number_input(
        key="condition_query_time", label="Choose time", min_value=1
    )
with col4:
    st.write("")
    condition_query_button = st.button(
        key="condition_query_button", label="Calculate condition query"
    )

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
        action_durations = list_of_actions.split(",")
        action_names = [
            action_duration.split(";")[0] for action_duration in action_durations
        ]
        action_durations_values = [
            action_duration.split(";")[1] for action_duration in action_durations
        ]
        st.text("Actions (duration)")
        for action in action_names:
            st.text(
                "- "
                + action
                + " ("
                + action_durations_values[action_names.index(action)]
                + ")"
            )

    if len(list_of_statements) == 0:
        st.text("--- no statements inserted ---")
    else:
        st.text("Statements")
        for statement in list_of_statements.split(","):
            stmnt = statement.split(";")
            statement_fluents_description = (
                stmnt[2].replace("#", " = ").replace(":", " AND ")
            )
            statement_condtions_description = (
                stmnt[3].replace("#", " = ").replace(":", " AND ")
            )
            if stmnt[1] != "impossible":
                st.text(
                    f"ACTION {stmnt[0]} {stmnt[1]} FLUENT {statement_fluents_description} GIVEN THAT {statement_condtions_description}"
                )
            else:
                st.write(stmnt)
                st.text(
                    f"ACTION {stmnt[0]} {stmnt[1]} GIVEN THAT {statement_condtions_description}"
                )
    action_durations = list_of_actions.split(",")

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
            st.text(f"- {obs[0]}={obs[1]} ({obs[2]})")

    if len(list_of_action_occurences) == 0:
        st.text("--- no action occurences inserted ---")
    else:
        st.text("Action occurences")
        for action_occurence in list_of_action_occurences.split(","):
            act = action_occurence.split(";")
            st.text(f"- {act[0]}={act[1]}")

    # model preparation

    calculate_button = st.button("Calculate model")

    if calculate_button:
        m = TimeDomainDescription()
        if len(list_of_initial_states) > 0:
            for initial_state in list_of_initial_states.split(","):
                state = initial_state.split(";")
                m.initially(**{state[0]: state[1] == "True"})
        if len(list_of_actions) > 0:
            for duration in list_of_actions.split(","):
                state = duration.split(";")
                m.duration(state[0], int(state[1]))
        if len(list_of_statements) > 0:
            for statement in list_of_statements.split(","):
                stmnt = statement.split(";")
                if stmnt[1] == "causes" or stmnt[1] == "releases":
                    statement_fluents_model = stmnt[2].split(":")
                    fluent_values_model = []
                    for i in statement_fluents_model:
                        fluent_values_model.append(
                            Fluent(**{i.split("#")[0]: i.split("#")[1] == "True"})
                        )

                statement_conditions_model = stmnt[3].split(":")
                condition_values_model = []
                try:
                    for i in statement_conditions_model:
                        condition_values_model.append(
                            Fluent(**{i.split("#")[0]: i.split("#")[1] == "True"})
                        )
                except:
                    pass

                if stmnt[1] == "causes":
                    m.causes(
                        stmnt[0],
                        fluent_values_model,
                        conditions=condition_values_model,
                    )
                elif stmnt[1] == "releases":
                    m.releases(stmnt[0], fluent_values_model)
                elif stmnt[1] == "impossible":
                    m.impossible(stmnt[0], conditions=condition_values_model)

        if len(list_of_observations) > 0:
            OBS_list = []
            for observation in list_of_observations.split(","):
                obs = observation.split(";")
                OBS_list.append(Fluent(**{obs[0]: obs[1] == "True"}))
            OBS = (OBS_list, int(obs[2]))

        if len(list_of_action_occurences) > 0:
            ACS_list = []
            for action in list_of_action_occurences.split(","):
                acs = action.split(";")
                ACS_list.append((acs[0], int(acs[1])))
            ACS = tuple(ACS_list)

        with Capturing() as output:
            m.description()
        st.write(output)

        try:
            s = Scenario(domain=m, observations=OBS, action_occurances=ACS)
        except NameError:
            s = None

        try:
            with Capturing() as output:
                s_result = s.is_consistent(verbose=True)
            st.write(output)
            st.write(f"Is consistent: {s_result}")
        except Exception as e:
            pass
            # st.write(f"Your mistake: {e}")
