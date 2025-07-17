import pygame

class Quest:
    def __init__(self, quest_id, name, description, quest_type, requirements):
        self.id = quest_id
        self.name = name
        self.description = description
        self.type = quest_type  # 'collect', 'kill', 'talk', 'deliver'
        self.requirements = requirements
        self.progress = {}
        self.completed = False
        self.active = True
        
        # Initialize progress based on quest type
        if quest_type == 'collect':
            for item, amount in requirements.items():
                self.progress[item] = 0

class QuestSystem:
    def __init__(self):
        self.quests = {}
        self.completed_quests = []
        self.inventory = {}

    def add_quest(self, quest_id, name, description, requirements):
        if quest_id not in self.quests:
            quest_type = 'collect'  # Default type, can be expanded
            quest = Quest(quest_id, name, description, quest_type, requirements)
            self.quests[quest_id] = quest
            return True
        return False

    def has_quest(self, quest_id):
        return quest_id in self.quests

    def get_active_quests(self):
        active_quests = []
        for quest in self.quests.values():
            if quest.active and not quest.completed:
                quest_data = {
                    'id': quest.id,
                    'name': quest.name,
                    'description': quest.description,
                    'type': quest.type,
                    'requirements': quest.requirements,
                    'progress': quest.progress
                }
                active_quests.append(quest_data)
        return active_quests

    def get_quest_progress(self, quest_id):
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            if quest.type == 'collect':
                # Return total collected items
                return sum(quest.progress.values())
        return 0

    def update_quest_progress(self, quest_id, item, amount=1):
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            if quest.type == 'collect' and item in quest.requirements:
                quest.progress[item] = min(quest.progress[item] + amount, quest.requirements[item])
                self._check_quest_completion(quest_id)

    def _check_quest_completion(self, quest_id):
        quest = self.quests[quest_id]
        if quest.type == 'collect':
            completed = True
            for item, required_amount in quest.requirements.items():
                if quest.progress[item] < required_amount:
                    completed = False
                    break
            
            if completed:
                quest.completed = True
                quest.active = False
                self.completed_quests.append(quest_id)
                return True
        return False

    def add_item_to_inventory(self, item, amount=1):
        if item in self.inventory:
            self.inventory[item] += amount
        else:
            self.inventory[item] = amount
        
        # Update quest progress for all active collect quests
        for quest in self.quests.values():
            if quest.active and quest.type == 'collect' and item in quest.requirements:
                self.update_quest_progress(quest.id, item, amount)

    def get_inventory(self):
        return self.inventory.copy()

    def remove_item_from_inventory(self, item, amount=1):
        if item in self.inventory:
            self.inventory[item] = max(0, self.inventory[item] - amount)
            if self.inventory[item] == 0:
                del self.inventory[item]

    def is_quest_completed(self, quest_id):
        return quest_id in self.completed_quests

    def get_completed_quests(self):
        return self.completed_quests.copy()