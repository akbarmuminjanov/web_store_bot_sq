from loader import dp
from .chatadmin import AdminFilter
from .group import IsGroup

if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    
