class ConfigurationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.quiz_settings = {
            'time_limit': 30,
            'passing_score': 70,
            'max_attempts': 3
        }
        self.email_settings = {
            'sender': 'noreply@medicalquiz.com',
            'templates': {
                'welcome': 'welcome_template',
                'quiz_completed': 'quiz_completed_template'
            }
        }
