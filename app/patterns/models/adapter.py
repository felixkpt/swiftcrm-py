import bcrypt
from app.models.social_media.conversation.categories.sub_categories.sub_category_model import SocialMediaConversationCategoriesSubCategory as SubCategoryModel
from app.models.social_media.conversation.categories.sub_categories.questions.question_model import Soc4eiaConversationCategoriesSubCategoriesQuestion as QuestionRepo
from app.models.users.user_model import User as UserRepo
from app.models.social_media.conversation.categories.category_model import SocialMediaConversationCategory as CategoryRepo

class ModelAdapter:
    def __init__(self, data):
        self.data = data
    
    def adapt_admin_user(self):
        hashed_password = bcrypt.hashpw(self.data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return UserRepo(
            username=self.data['username'],
            email=self.data['email'],
            password=hashed_password
        )
    
    def adapt_category(self):
        return CategoryRepo(
            **self.data
        )
    
    def adapt_sub_category(self):
        return SubCategoryModel(
            category_id=self.data['category_id'],
            name=self.data['name'],
            learn_instructions=self.data['learn_instructions']['content']
        )
    
    def adapt_question(self):
        return QuestionRepo(
            category_id=self.data['category_id'],
            sub_category_id=self.data['sub_category_id'],
            question=self.data['question'],
            marks=self.data['marks']
        )
