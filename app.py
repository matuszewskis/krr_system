from io import StringIO
import sys
import streamlit as st
from krr_system import (
    TimeDomainDescription,
    Fluent,
    Scenario,
)
from sympy import Symbol, And, Or, Not
from sympy.logic.boolalg import Implies, Xnor, BooleanFunction

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


def formula_representation(formula_list):
    elements = []
    formula_list_split = formula_list.split(":")
    for element in formula_list_split:
        if element in ["AND", "OR", "IMPLIES", "IFF"]:
            if len(elements) < 2:
                return None
            combination = f"({elements[-2]} {element} {elements[-1]})"
            elements = elements[:-2]
            elements.append(combination)
        elif element == "NOT":
            if len(elements) < 1:
                return None
            elements[-1] = f"NOT {elements[-1]}"
        else:
            elements.append(element)
    if len(elements) == 1:
        return elements[0]
    return ', '.join(elements)

def formula_to_boolean(formula_list):
    if len(formula_list) == 0:
        return None
    elements = []
    formula_list_split = formula_list.split(":")
    for element in formula_list_split:
        if element in ["AND", "OR", "IMPLIES", "IFF"]:
            if len(elements) < 2:
                return None
            if element=="AND":
                combination = elements[-2] & elements[-1]
            elif element=="OR":
                combination = elements[-2] | elements[-1]
            elif element=="IMPLIES":
                combination = elements[-2] >> elements[-1]
            else:
                combination = Xnor(elements[-2], elements[-1])
            elements = elements[:-2]
            elements.append(combination)
        elif element == "NOT":
            if len(elements) < 1:
                return None
            elements[-1] = ~elements[-1]
        else:
            elements.append(Symbol(element))
    if len(elements) == 1:
        return elements[0]
    return None

def is_formula_valid(formula_list):
    return (formula_to_boolean(formula_list) is not None)


file_fluents = open("variables/fluents.txt", "r")
list_of_fluents = file_fluents.read()

file_actions = open("variables/actions.txt", "r")
list_of_actions = file_actions.read()

file_statements = open("variables/statements.txt", "r")
list_of_statements = file_statements.read()

file_initial_states = open("variables/initial_states.txt", "r")
list_of_initial_states = file_initial_states.read()

file_termination_time = open("variables/termination_time.txt", "r")
termination_time_value = file_termination_time.read()

file_observations = open("variables/observations.txt", "r")
list_of_observations = file_observations.read()

file_action_occurrences = open("variables/action_occurrences.txt", "r")
list_of_action_occurrences = file_action_occurrences.read()

file_technical_vars = open("variables/technical_variables.txt", "r")
list_of_technical_vars = file_technical_vars.read()

file_cause_formula = open("variables/cause_formula.txt", "r")
cause_formula = file_cause_formula.read()

file_statement_condition = open("variables/statement_condition.txt", "r")
statement_condition = file_statement_condition.read()

file_initial_condition = open("variables/initial_condition.txt", "r")
initial_condition = file_initial_condition.read()

file_observation_formula = open("variables/observation_formula.txt", "r")
observation_formula = file_observation_formula.read()

file_condition_query = open("variables/condition_query.txt", "r")
condition_query = file_condition_query.read()

file_fluents.close()
file_actions.close()
file_statements.close()
file_initial_states.close()
file_termination_time.close()
file_observations.close()
file_action_occurrences.close()
file_technical_vars.close()
file_cause_formula.close()
file_statement_condition.close()
file_initial_condition.close()
file_observation_formula.close()
file_condition_query.close()

st.title("Knowledge Representation and Reasoning")

st.header("Project D: Actions with Duration")

reset_button = st.button(label="Reset environment")

st.header("Domain Description")
if reset_button:
    list_of_fluents = ""
    list_of_actions = ""
    list_of_statements = ""
    list_of_initial_states = ""
    termination_time_value = ""
    list_of_observations = ""
    list_of_action_occurrences = ""
    list_of_technical_vars = "1;1"
    cause_formula = ""
    statement_condition = ""
    initial_condition = ""
    observation_formula = ""
    condition_query = ""
    file_fluents = open("variables/fluents.txt", "w")
    file_actions = open("variables/actions.txt", "w")
    file_statements = open("variables/statements.txt", "w")
    file_initial_states = open("variables/initial_states.txt", "w")
    file_termination_time = open("variables/termination_time.txt", "w")
    file_observations = open("variables/observations.txt", "w")
    file_action_occurrences = open("variables/action_occurrences.txt", "w")
    file_technical_vars = open("variables/technical_variables.txt", "w")
    file_cause_formula = open("variables/cause_formula.txt", "w")
    file_statement_condition = open("variables/statement_condition.txt", "w")
    file_initial_condition = open("variables/initial_condition.txt", "w")
    file_observation_formula = open("variables/observation_formula.txt", "w")
    file_condition_query = open("variables/condition_query.txt", "w")
    file_fluents.write("")
    file_actions.write("")
    file_statements.write("")
    file_initial_states.write("")
    file_termination_time.write("")
    file_observations.write("")
    file_action_occurrences.write("")
    file_technical_vars.write("1;1")
    file_cause_formula.write("")
    file_statement_condition.write("")
    file_initial_condition.write("")
    file_observation_formula.write("")
    file_condition_query.write("")
    file_fluents.close()
    file_actions.close()
    file_statements.close()
    file_initial_states.close()
    file_termination_time.close()
    file_observations.close()
    file_action_occurrences.close()
    file_technical_vars.close()
    file_cause_formula.close()
    file_statement_condition.close()
    file_initial_condition.close()
    file_observation_formula.close()
    file_condition_query.close()

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

    file_actions = open("variables/actions.txt", "w")

    if len(list_of_actions) == 0:
        file_actions.write(action_couple)
        list_of_actions += action_couple
    else:
        list_of_actions_splitted = list_of_actions.split(",")
        action_names = [action.split(";")[0] for action in list_of_actions_splitted]
        duration_values = [action.split(";")[1] for action in list_of_actions_splitted]
        if action_input in action_names:
            action_index = action_names.index(action_input)
            duration_values[action_index] = str(duration_input)
        else:
            action_names.append(action_input)
            duration_values.append(duration_input)
        new_durations = [
            f"{action_names[i]};{duration_values[i]}"
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
col1, col2, col3, col4 = st.columns([4, 4, 6, 6])

with col1:
    statement_action = st.selectbox(
        "Choose action", [action.split(";")[0] for action in list_of_actions.split(",")]
    )
with col2:
    statement_type = st.selectbox(
        "Statement type", ["causes", "releases", "impossible"]
    )
with col3:
    st.write("**Cause formula**")
    if statement_type == "causes":
        col3a, col3b = st.columns([2, 1])
        with col3a:
            statement_cause_select_fluent = st.selectbox(
                "Choose fluent", list_of_fluents.split(","),
                key="statement_cause_select_fluent"
            )
        with col3b:
            st.write("")
            st.write("")
            statement_cause_submit_fluent = st.button(
                label="Add",
                key="statement_cause_submit_fluent"
            )
        col3c, col3d = st.columns([2, 1])
        with col3c:
            statement_cause_select_operator = st.selectbox(
                "Choose operator", ["NOT", "AND", "OR", "IMPLIES", "IFF"],
                key="statement_cause_select_operator"
            )
        with col3d:
            st.write("")
            st.write("")
            statement_cause_submit_operator = st.button(
                label="Add",
                key="statement_cause_submit_operator"
            )
        col3e, col3f = st.columns([2, 3])
        with col3e:
            statement_cause_undo = st.button(
                label="Undo",
                key="statement_cause_undo"
            )
        with col3f:
            statement_cause_clear = st.button(
                label="Clear",
                key="statement_cause_clear"
            )
        
        if statement_cause_submit_fluent:
            if len(cause_formula) > 0:
                cause_formula += ":"
            cause_formula += statement_cause_select_fluent
        if statement_cause_submit_operator:
            if len(cause_formula) > 0:
                cause_formula += ":"
            cause_formula += statement_cause_select_operator
        if statement_cause_undo:
            if ":" in cause_formula:
                colon_index = cause_formula.rfind(":")
                cause_formula = cause_formula[:colon_index]
            else:
                cause_formula = ""
        if statement_cause_clear:
            cause_formula = ""
        st.write(formula_representation(cause_formula))
        
    elif statement_type == "releases":
        statement_release_fluent = st.selectbox(
            "Choose released fluent", list_of_fluents.split(",")
        )

with col4:
    st.write("**Condition**")
    col4a, col4b = st.columns([2, 1])
    with col4a:
        statement_condition_select_fluent = st.selectbox(
            "Choose fluent", list_of_fluents.split(","),
            key="statement_condition_select_fluent"
        )
    with col4b:
        st.write("")
        st.write("")
        statement_condition_submit_fluent = st.button(
            label="Add",
            key="statement_condition_submit_fluent"
        )
    col4c, col4d = st.columns([2, 1])
    with col4c:
        statement_condition_select_operator = st.selectbox(
            "Choose operator", ["NOT", "AND", "OR", "IMPLIES", "IFF"],
            key="statement_condition_select_operator"
        )
    with col4d:
        st.write("")
        st.write("")
        statement_condition_submit_operator = st.button(
            label="Add",
            key="statement_condition_submit_operator"
        )
    col4e, col4f = st.columns([2, 3])
    with col4e:
        statement_condition_undo = st.button(
            label="Undo",
            key="statement_condition_undo"
        )
    with col4f:
        statement_condition_clear = st.button(
            label="Clear",
            key="statement_condition_clear"
        )
    
    if statement_condition_submit_fluent:
        if len(statement_condition) > 0:
            statement_condition += ":"
        statement_condition += statement_condition_select_fluent
    if statement_condition_submit_operator:
        if len(statement_condition) > 0:
            statement_condition += ":"
        statement_condition += statement_condition_select_operator
    if statement_condition_undo:
        if ":" in statement_condition:
            colon_index = statement_condition.rfind(":")
            statement_condition = statement_condition[:colon_index]
        else:
            statement_condition = ""
    if statement_condition_clear:
        statement_condition = ""
    st.write(formula_representation(statement_condition))

submit_button = st.text("")
submit_button = st.button(label="Submit statement")

file_technical_vars = open("variables/technical_variables.txt", "w")
file_technical_vars.write(f"{condition_values};{fluent_values}")
file_technical_vars.close()
file_cause_formula = open("variables/cause_formula.txt", "w")
file_cause_formula.write(cause_formula)
file_cause_formula.close()
file_statement_condition = open("variables/statement_condition.txt", "w")
file_statement_condition.write(statement_condition)
file_statement_condition.close()

is_statement_valid_to_submit = is_formula_valid(statement_condition)
if statement_type != "impossible" and statement_type != "releases":
    is_statement_valid_to_submit = is_statement_valid_to_submit and is_formula_valid(cause_formula)

if submit_button:
    if is_statement_valid_to_submit:
        if statement_type != "impossible" and statement_type != "releases":
            statement_quartet = f"{statement_action};{statement_type};{cause_formula};{statement_condition}"
        elif statement_type != "impossible":
            statement_quartet = f"{statement_action};{statement_type};{statement_release_fluent};{statement_condition}"
        else:
            statement_quartet = (f"{statement_action};{statement_type};;{statement_condition}")

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
    elif not is_formula_valid(statement_condition):
        st.write("Invalid statement condition")
    elif statement_type != "impossible" and statement_type != "releases" and not is_formula_valid(cause_formula):
        st.write("Invalid cause formula")

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

# time termination

st.subheader("Termination")
col1, col2 = st.columns([3, 1])

with col1:
    termination_time_input = st.number_input(label="Input termination time", min_value=1, step=1, value=10)
with col2:
    st.write("")
    termination_time = st.button(label="Submit termination time")

if termination_time:
    file_termination_time = open("variables/termination_time.txt", "w")
    file_termination_time.write(str(termination_time_input))
    termination_time_value = str(termination_time_input)
    file_termination_time.close()

st.header("Scenario")

# observations input

st.subheader("Observations")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    st.write("**Formula**")
    col1a, col1b = st.columns([4, 1])
    with col1a:
        observation_formula_select_fluent = st.selectbox(
            "Choose fluent", list_of_fluents.split(","),
            key="observation_select_fluent"
        )
    with col1b:
        st.write("")
        st.write("")
        observation_formula_submit_fluent = st.button(
            label="Add",
            key="observation_submit_fluent"
        )
    col1c, col1d = st.columns([4, 1])
    with col1c:
        observation_formula_select_operator = st.selectbox(
            "Choose operator", ["NOT", "AND", "OR", "IMPLIES", "IFF"],
            key="observation_select_operator"
        )
    with col1d:
        st.write("")
        st.write("")
        observation_formula_submit_operator = st.button(
            label="Add",
            key="observation_submit_operator"
        )
    col1e, col1f = st.columns([1, 3])
    with col1e:
        observation_formula_undo = st.button(
            label="Undo",
            key="observation_formula_undo"
        )
    with col1f:
        observation_formula_clear = st.button(
            label="Clear",
            key="observation_formula_clear"
        )

    if observation_formula_submit_fluent:
        if len(observation_formula) > 0:
            observation_formula += ":"
        observation_formula += observation_formula_select_fluent
    if observation_formula_submit_operator:
        if len(observation_formula) > 0:
            observation_formula += ":"
        observation_formula += observation_formula_select_operator
    if observation_formula_undo:
        if ":" in observation_formula:
            colon_index = observation_formula.rfind(":")
            observation_formula = observation_formula[:colon_index]
        else:
            observation_formula = ""
    if observation_formula_clear:
        observation_formula = ""
    st.write(formula_representation(observation_formula))
with col2:
    observation_formula_time = st.number_input(
        key="observation_formula_time", label="Choose observation time", min_value=1
    )
with col3:
    st.write("")
    observation = st.button(label="Submit observation")

file_observation_formula = open("variables/observation_formula.txt", "w")
file_observation_formula.write(observation_formula)
file_observation_formula.close()

if observation:
    if is_formula_valid(observation_formula):
        observation_couple = (
            f"{observation_formula};{observation_formula_time}"
        )

        file_observations = open("variables/observations.txt", "a")

        if len(list_of_observations) == 0:
            file_observations.write(observation_couple)
            list_of_observations += observation_couple
        else:
            existing_observations = list_of_observations.split(",")
            if observation_couple not in existing_observations:
                file_observations.write("," + observation_couple)
                list_of_observations += "," + observation_couple
        file_observations.close()
    else:
        st.write("Invalid observation formula")

# action occurrences input

st.subheader("Action occurrences")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    action_occurrence = st.selectbox(
        key="action_occurrence",
        label="Choose action occurrence",
        options=[action.split(";")[0] for action in list_of_actions.split(",")],
    )
with col2:
    action_occurrence_time = st.number_input(
        key="action_occurrence_time", label="Choose occurrence time", min_value=1
    )
with col3:
    st.write("")
    action_occurrence_button = st.button(label="Submit action occurrence")

if action_occurrence_button:
    action_occurrence_couple = f"{action_occurrence};{action_occurrence_time}"

    file_action_occurrences = open("variables/action_occurrences.txt", "a")
    st.write()
    if len(list_of_action_occurrences) == 0:
        file_action_occurrences.write(action_occurrence_couple)
        list_of_action_occurrences += action_occurrence_couple
    else:
        list_of_action_occurrence_times = [
            ac.split(";")[1] for ac in list_of_action_occurrences.split(",")
        ]
        if action_occurrence_time not in list_of_action_occurrence_times:
            file_action_occurrences.write("," + action_occurrence_couple)
            list_of_action_occurrences += "," + action_occurrence_couple

st.header("Queries")

def scenario_calculation():
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
                formula_model = formula_to_boolean(stmnt[2])

            condition_model = formula_to_boolean(stmnt[3])

            if stmnt[1] == "causes":
                m.causes(stmnt[0], formula_model, conditions=condition_model)
            elif stmnt[1] == "releases":
                m.releases(stmnt[0], formula_model, conditions=condition_model)
            elif stmnt[1] == "impossible":
                m.impossible(stmnt[0], conditions=condition_model)
    if len(termination_time_value) > 0:
        m.terminate_time(int(termination_time_value))

    if len(list_of_observations) > 0:
        OBS = []
        for observation in list_of_observations.split(","):
            obs = observation.split(";")
            obs_tuple = (formula_to_boolean(obs[0]), int(obs[1]))
        OBS.append(obs_tuple)

    if len(list_of_action_occurrences) > 0:
        ACS_list = []
        for action in list_of_action_occurrences.split(","):
            acs = action.split(";")
            ACS_list.append((acs[0], int(acs[1])))
        ACS = tuple(ACS_list)

    with Capturing() as output:
        m.description()
    st.write(output)
    
    try:
        s = Scenario(domain=m, observations=OBS, action_occurrences=ACS)
    except NameError:
        s = None
    return s
    
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

if action_query_button:
    s = scenario_calculation()
    try:
        with Capturing() as output:
            s_result = s.is_consistent(verbose=True)
            if s_result:
                a_result = s.does_action_perform(action_query, action_query_time)
            else:
                a_result = False
        st.write(output)
        st.write(f"Does action perform: {a_result}")
    except Exception as e:
        st.write(f"Your mistake: {e}")


# condition query

st.subheader("Condition query")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    st.write("**Formula**")
    col1a, col1b = st.columns([4, 1])
    with col1a:
        condition_query_select_fluent = st.selectbox(
            "Choose fluent", list_of_fluents.split(","),
            key="condition_query_select_fluent"
        )
    with col1b:
        st.write("")
        st.write("")
        condition_query_submit_fluent = st.button(
            label="Add",
            key="condition_query_submit_fluent"
        )
    col1c, col1d = st.columns([4, 1])
    with col1c:
        condition_query_select_operator = st.selectbox(
            "Choose operator", ["NOT", "AND", "OR", "IMPLIES", "IFF"],
            key="condition_query_select_operator"
        )
    with col1d:
        st.write("")
        st.write("")
        condition_query_submit_operator = st.button(
            label="Add",
            key="condition_query_submit_operator"
        )
    col1e, col1f = st.columns([1, 3])
    with col1e:
        condition_query_undo = st.button(
            label="Undo",
            key="condition_query_undo"
        )
    with col1f:
        condition_query_clear = st.button(
            label="Clear",
            key="condition_query_clear"
        )

    if condition_query_submit_fluent:
        if len(condition_query) > 0:
            condition_query += ":"
        condition_query += condition_query_select_fluent
    if condition_query_submit_operator:
        if len(condition_query) > 0:
            condition_query += ":"
        condition_query += condition_query_select_operator
    if condition_query_undo:
        if ":" in condition_query:
            colon_index = condition_query.rfind(":")
            condition_query = condition_query[:colon_index]
        else:
            condition_query = ""
    if condition_query_clear:
        condition_query = ""
    st.write(formula_representation(condition_query))
with col2:
    condition_query_time = st.number_input(
        key="condition_query_time", label="Choose time", min_value=1
    )
with col3:
    st.write("")
    condition_query_button = st.button(
        key="condition_query_button", label="Calculate condition query"
    )

if condition_query_button:
    if is_formula_valid(condition_query):
        s = scenario_calculation()
        try:
            with Capturing() as output:
                s_result = s.is_consistent()
                if s_result:
                    q_result = s.check_if_condition_hold(formula_to_boolean(condition_query), condition_query_time, verbose=True)
                else:
                    q_result = False
            st.write(output)
            if q_result is None:
                st.write("Condition possible, but unnecessary")
            elif q_result:
                st.write("Condition necessary")
            else:
                st.write("Condition impossible")
        except Exception as e:
            st.write(f"Your mistake: {e}")
    else:
        st.write("Invalid condition query formula")

file_condition_query = open("variables/condition_query.txt", "w")
file_condition_query.write(condition_query)
file_condition_query.close()

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
            statement_formula_description = formula_representation(stmnt[2])
            statement_condtions_description = formula_representation(stmnt[3])
            if_word = ' if '
            if len(statement_condtions_description)==0:
                if_word = ''
            if stmnt[1] != "impossible":
                st.text(
                    f"{stmnt[0]} {stmnt[1]} {statement_formula_description}{if_word}{statement_condtions_description}"
                )
            else:
                st.write(stmnt)
                st.text(
                    f"{stmnt[0]} {stmnt[1]}{if_word}{statement_condtions_description}"
                )
    action_durations = list_of_actions.split(",")

    if len(list_of_initial_states) == 0:
        st.text("--- no initial values inserted ---")
    else:
        st.text("Initial state")
        for initial_state in list_of_initial_states.split(","):
            state = initial_state.split(";")
            st.text(f"- {state[0]}={state[1]}")

    if len(termination_time_value) == 0:
        st.text("--- termination time not set ---")
    else:
        st.text("Termination time")
        st.text(f"- {termination_time_value}")

    if len(list_of_observations) == 0:
        st.text("--- no observations inserted ---")
    else:
        st.text("Observations")
        for observation in list_of_observations.split(","):
            obs = observation.split(";")
            st.text(f"- {formula_representation(obs[0])} ({obs[1]})")

    if len(list_of_action_occurrences) == 0:
        st.text("--- no action occurrences inserted ---")
    else:
        st.text("Action occurrences")
        for action_occurrence in list_of_action_occurrences.split(","):
            act = action_occurrence.split(";")
            st.text(f"- {act[0]}={act[1]}")

    # model preparation

    calculate_button = st.button("Calculate model")

    if calculate_button:
        s = scenario_calculation()
        try:
            with Capturing() as output:
                s_result = s.is_consistent(verbose=True)
            st.write(output)
            st.write(f"Is consistent: {s_result}")
        except Exception as e:
            pass
            # st.write(f"Your mistake: {e}")
