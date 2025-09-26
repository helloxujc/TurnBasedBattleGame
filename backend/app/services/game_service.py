from typing import Dict, Any
import random
from app.models.character import Character, CharacterType
from app.models.game import GameSession, GameState, ActionType, GameAction

class GameService:
    def create_character(self, character_type: str) -> Character:
        return Character.create_character(CharacterType(character_type))

    def get_random_character_type(self) -> str:
        # Assign a random character type for AI opponent
        return random.choice([CharacterType.WARRIOR, CharacterType.TANKER, CharacterType.MAGE])

    async def process_player_vs_ai_turn(self, session: GameSession, player_action_type: str) -> Dict[str, Any]:
        if not session.is_ready():
            return {"error": "Game not ready"}

        # Process player action
        player_action = self._execute_action(session.player.character, ActionType(player_action_type))

        # Generate AI action
        ai_action_type = self._get_ai_action(session.ai_opponent.character)
        ai_action = self._execute_action(session.ai_opponent.character, ai_action_type)

        # Resolve combat
        result = self._resolve_player_vs_ai_combat(session, player_action, ai_action)

        # Update turn counter for skill cooldown
        session.player.character.turns_since_last_skill += 1
        session.ai_opponent.character.turns_since_last_skill += 1

        # Add turn to history
        turn_summary = result["summary"]
        session.turn_history.append(turn_summary)
        session.current_turn += 1

        # Check for game over
        if not session.player.character.is_alive():
            session.state = GameState.FINISHED
            session.winner = "AI"
        elif not session.ai_opponent.character.is_alive():
            session.state = GameState.FINISHED
            session.winner = session.player.id
        else:
            # Continue game
            session.state = GameState.AI_TURN
            session.state = GameState.PLAYER_TURN

        return result

    def _execute_action(self, character: Character, action_type: ActionType) -> GameAction:
        if action_type == ActionType.ATTACK:
            damage = character.attack()
            return GameAction(
                action_type=action_type,
                damage_dealt=damage
            )
        elif action_type == ActionType.DEFEND:
            defense = character.defend()
            return GameAction(
                action_type=action_type,
                defense_value=defense
            )
        elif action_type == ActionType.SKILL:
            if character.can_use_skill():
                damage, defense = character.use_skill()
                return GameAction(
                    action_type=action_type,
                    damage_dealt=damage,
                    defense_value=defense
                )
            else:
                # Fallback to basic attack if skill is on cooldown
                damage = character.attack()
                return GameAction(
                    action_type=ActionType.ATTACK,
                    damage_dealt=damage
                )

    def _get_ai_action(self, character: Character) -> ActionType:
        import random

        # Low health - prefer defensive actions
        health_percentage = character.current_hp / character.max_hp

        if health_percentage < 0.3:
            # Low health - prefer skill or defend
            if character.can_use_skill() and random.random() < 0.6:
                return ActionType.SKILL
            elif random.random() < 0.5:
                return ActionType.DEFEND
            else:
                return ActionType.ATTACK

        elif health_percentage < 0.7:
            # Medium health - balanced approach
            if character.can_use_skill() and random.random() < 0.4:
                return ActionType.SKILL
            elif random.random() < 0.3:
                return ActionType.DEFEND
            else:
                return ActionType.ATTACK

        else:
            # High health - prefer attacks
            if character.can_use_skill() and random.random() < 0.3:
                return ActionType.SKILL
            elif random.random() < 0.2:
                return ActionType.DEFEND
            else:
                return ActionType.ATTACK

    def _resolve_player_vs_ai_combat(self, session: GameSession, player_action: GameAction, ai_action: GameAction) -> Dict[str, Any]:
        """Resolve combat between player and AI"""

        # Calculate actual damage dealt
        player_damage = player_action.damage_dealt
        ai_damage = ai_action.damage_dealt

        # Apply defense
        if ai_action.defense_value > 0:
            player_damage = max(0, player_damage - ai_action.defense_value)
        if player_action.defense_value > 0:
            ai_damage = max(0, ai_damage - player_action.defense_value)

        # Apply damage
        session.player.character.take_damage(ai_damage)
        session.ai_opponent.character.take_damage(player_damage)

        # Update action records
        player_action.damage_taken = ai_damage
        ai_action.damage_taken = player_damage

        # Generate summary
        summary = self._generate_combat_summary(session, player_action, ai_action)

        return {
            "player_action": player_action.dict(),
            "ai_action": ai_action.dict(),
            "player_hp": session.player.character.current_hp,
            "ai_hp": session.ai_opponent.character.current_hp,
            "summary": summary
        }

    def _generate_combat_summary(self, session: GameSession, player_action: GameAction, ai_action: GameAction) -> str:
        # Generate a readable summary of the combat
        player_name = session.player.character.name
        ai_name = session.ai_opponent.character.name

        summary_parts = []

        # Player action
        if player_action.action_type == ActionType.ATTACK:
            summary_parts.append(f"You attack for {player_action.damage_dealt} damage")
        elif player_action.action_type == ActionType.DEFEND:
            summary_parts.append(f"You defend (+{player_action.defense_value} defense)")
        elif player_action.action_type == ActionType.SKILL:
            skill_name = session.player.character.skill_name
            if player_action.damage_dealt > 0:
                summary_parts.append(f"You use {skill_name} for {player_action.damage_dealt} damage")
            else:
                summary_parts.append(f"You use {skill_name} (+{player_action.defense_value} defense)")

        # AI action
        if ai_action.action_type == ActionType.ATTACK:
            summary_parts.append(f"AI {ai_name} attacks for {ai_action.damage_dealt} damage")
        elif ai_action.action_type == ActionType.DEFEND:
            summary_parts.append(f"AI {ai_name} defends (+{ai_action.defense_value} defense)")
        elif ai_action.action_type == ActionType.SKILL:
            skill_name = session.ai_opponent.character.skill_name
            if ai_action.damage_dealt > 0:
                summary_parts.append(f"AI {ai_name} uses {skill_name} for {ai_action.damage_dealt} damage")
            else:
                summary_parts.append(f"AI {ai_name} uses {skill_name} (+{ai_action.defense_value} defense)")

        # Add damage results
        if player_action.damage_taken > 0:
            summary_parts.append(f"You take {player_action.damage_taken} damage")
        if ai_action.damage_taken > 0:
            summary_parts.append(f"AI takes {ai_action.damage_taken} damage")

        return ". ".join(summary_parts)