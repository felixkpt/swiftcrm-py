import bcrypt
from app.models.conversation.v2.categories.sub_categories.sub_category import ConversationV2CategoriesSubCategory
from app.models.conversation.v2.categories.sub_categories.questions.question import ConversationV2CategoriesSubCategoriesQuestion
# from app.models.admin.users.user import AdminUser
from app.models.conversation.v2.categories.category import ConversationV2Category

class ModelAdapter:
    def __init__(self, data):
        self.data = data
    
    def adapt_admin_user(self):
        hashed_password = bcrypt.hashpw(self.data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return AdminUser(
            username=self.data['username'],
            email=self.data['email'],
            password=hashed_password
        )
    
    def adapt_category(self):
        return ConversationV2Category(
            **self.data
        )
    
    def adapt_sub_category(self):
        return ConversationV2CategoriesSubCategory(
            category_id=self.data['category_id'],
            name=self.data['name'],
            learn_instructions=self.data['learn_instructions']['content']
        )
    
    def adapt_question(self):
        return ConversationV2CategoriesSubCategoriesQuestion(
            category_id=self.data['category_id'],
            sub_category_id=self.data['sub_category_id'],
            question=self.data['question'],
            marks=self.data['marks']
        )
