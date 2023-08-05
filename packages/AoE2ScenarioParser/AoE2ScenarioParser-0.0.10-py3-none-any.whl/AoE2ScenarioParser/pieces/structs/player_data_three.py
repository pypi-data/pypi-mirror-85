from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
from AoE2ScenarioParser.helper.retriever_dependency import RetrieverDependency, DependencyAction, DependencyEval, \
    DependencyTarget
from AoE2ScenarioParser.pieces.structs.aoe2_struct import AoE2Struct


class PlayerDataThreeStruct(AoE2Struct):
    def __init__(self, parser_obj=None, data=None):
        retrievers = [
            Retriever("constant_name", DataType("str16")),
            Retriever("initial_camera_x", DataType("f32")),
            Retriever("initial_camera_y", DataType("f32")),
            Retriever("unknown_similar_to_camera_x", DataType("s16")),
            Retriever("unknown_similar_to_camera_y", DataType("s16")),
            Retriever("aok_allied_victory", DataType("u8")),
            Retriever("player_count_for_diplomacy", DataType("u16"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_VALUE, DependencyTarget("self", "diplomacy_for_interaction"),
                          DependencyEval("len(x)"))),
            Retriever("diplomacy_for_interaction", DataType("u8"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_REPEAT, DependencyTarget("self", "player_count_for_diplomacy")),
                      on_construct=RetrieverDependency(DependencyAction.REFRESH_SELF),
                      on_commit=RetrieverDependency(
                          DependencyAction.REFRESH, DependencyTarget("self", "player_count_for_diplomacy"))),
            Retriever("diplomacy_for_ai_system", DataType("u32", repeat=9)),
            Retriever("color", DataType("u32")),
            Retriever("victory_version", DataType("f32"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_VALUE, DependencyTarget("self", "unknown_2"),
                          DependencyEval("2 if len(x) == 7 else 0"))),
            Retriever("unknown", DataType("u16"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_VALUE, DependencyTarget("self", "unknown_structure_grand_theft_empires"),
                          DependencyEval("len(x)"))),
            Retriever("unknown_2", DataType("u8"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_REPEAT, DependencyTarget("self", "victory_version"),
                          DependencyEval("7 if x == 2 else 0")),
                      on_construct=RetrieverDependency(DependencyAction.REFRESH_SELF),
                      on_commit=RetrieverDependency(
                          DependencyAction.REFRESH, DependencyTarget("self", "victory_version"))),
            Retriever("unknown_5", DataType("u8"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_REPEAT, DependencyTarget("self", "victory_version"),
                          DependencyEval("1 if x == 2 else 0")),
                      on_construct=RetrieverDependency(DependencyAction.REFRESH_SELF)),
            Retriever("unknown_structure_grand_theft_empires", DataType("44"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_REPEAT, DependencyTarget("self", "unknown")
                      ),
                      on_construct=RetrieverDependency(DependencyAction.REFRESH_SELF),
                      on_commit=RetrieverDependency(
                          DependencyAction.REFRESH, DependencyTarget("self", "unknown"))),
            Retriever("unknown_3", DataType("u8", repeat=7)),
            # Todo: Has to change value of unknown_5. But currently not supported
            Retriever("unknown_structure_ww_campaign_2", DataType("32"),
                      on_refresh=RetrieverDependency(
                          DependencyAction.SET_REPEAT, DependencyTarget("self", "unknown_5"),
                      DependencyEval("x[0]")),
                      on_construct=RetrieverDependency(DependencyAction.REFRESH_SELF)),
            Retriever("unknown_4", DataType("s32")),
        ]

        super().__init__("Player Data #3", retrievers, parser_obj, data)

    @staticmethod
    def defaults():
        defaults = {
            'constant_name': 'Scenario Editor Phantom',
            'initial_camera_x': 60.0,
            'initial_camera_y': 60.0,
            'unknown_similar_to_camera_x': 95,
            'unknown_similar_to_camera_y': 87,
            'aok_allied_victory': 0,
            'player_count_for_diplomacy': 9,
            'diplomacy_for_interaction': [3, 0, 3, 3, 3, 3, 3, 3, 3],
            'diplomacy_for_ai_system': [0, 1, 4, 4, 4, 4, 4, 4, 4],
            'color': 0,
            'victory_version': 2.0,
            'unknown': 0,
            'unknown_2': [0, 0, 0, 0, 0, 0, 0],
            'unknown_5': 0,
            'unknown_structure_grand_theft_empires': [],
            'unknown_3': [0, 0, 0, 0, 0, 0, 0],
            'unknown_structure_ww_campaign_2': [],
            'unknown_4': -1,
        }
        return defaults
