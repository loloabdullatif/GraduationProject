from django.urls import path
from graduationapp import views


urlpatterns = [
    # path("", views.create_account, name="index"),
    # path('create_account/', views.create_account, name='create_account'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout, name='logout'),
    # web urls
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('account', views.account, name='account'),
    path('addfarm', views.addfarm, name='addfarm'),
    path('addhotel', views.addhotel, name='addhotel'),
    path('addResturant', views.addResturant, name='addResturant'),
    path('addResturant/addtable/<int:resturant_id>',
         views.addtable, name='addtable'),
    path('book-room', views.book_room_page, name="bookroompage"),
    path('book-room/book', views.roombooking, name='roombooking'),
    path('dashbord/<int:hotel_id>', views.dashbord, name='dashbord'),
    path('dashbord_Table/<int:resturant_id>',
         views.dashbord_Table, name='dashbord_Table'),
    path('farm', views.farm, name='farm'),
    path('Resturant', views.Resturant, name='Resturant'),
    path('table/<int:resturant_id>', views.table, name='table'),
    path('hotel', views.hotel, name='hotel'),
    path('addhotel/addroom/<int:hotel_id>', views.addroom, name='addroom'),
    path('detailhotel/<int:hotel_id>',
         views.public_place_detail, name='public_place_detail'),
    path('detailfarm/<int:farm_id>', views.public_place_detail2,
         name='public_place_detail2'),
    path('detailres/<int:resturant_id>',
         views.public_place_detail3, name='public_place_detail3'),

    path('dashbord/delete-room/<int:roomid>',
         views.delete_room, name='delete_room'),

    path('room/<int:hotel_id>', views.room, name='room'),
    path('book-farm', views.book_farm_page, name="bookfarmpage"),
    path('book-farm/book', views.farmbooking, name='farmbooking'),
    path('book-table', views.book_table_page, name="booktablepage"),
    path('book-table/book', views.tablebooking, name='tablebooking'),
    path('mybooking', views.mybooking, name='mybooking'),
    path('yourplace', views.yourplace, name='yourplace'),
    path('updateinfo', views.updateinfo, name='updateinfo'),
    path('deletefarmbooking/<int:farmbooking_id>',
         views.delete_farmbooking, name='delete_farmbooking'),
    path('deleteroombooking/<int:roombooking_id>',
         views.delete_roombooking, name='delete_roombooking'),
    path('deletetablebooking/<int:tablebooking_id>',
         views.delete_tablebooking, name='delete_tablebooking'),
    path('deletepublicplace/<int:publicplace_id>',
         views.deletepublicplace, name='deletepublicplace'),


    path('adminpage', views.adminpage, name='adminpage'),
    path('approve-place/<int:publicplace_id>',
         views.approve_place, name='approve_place'),
    path('reject-place/<int:publicplace_id>',
         views.reject_place, name='reject_place'),
    path('allbookings/<int:farm_id>', views.allbookings, name='allbookings'),
    path('allroombookings/<int:hotel_id>',
         views.allroombookings, name='allroombookings'),
    path('alltablebookings/<int:rest_id>',
         views.alltablebookings, name='alltablebookings'),

    path('proposedPlaces', views.proposedplaces, name='proposedplaces'),

    path('delete_myroombooking/<int:roombooking_id>',
         views.delete_myroombooking, name='delete_myroombooking'),
    path('delete_mybookingfarm/<int:farmbooking_id>',
         views.delete_mybookingfarm, name='delete_mybookingfarm'),
    path('delete_mytablebooking/<int:tablebooking_id>',
         views.delete_mytablebooking, name='delete_mytablebooking'),


    path('DeleteAccount', views.DeleteAccount, name='DeleteAccount'),
    # path('UpdateAccount/', views.UpdateAccount, name='UpdateAccount'),

    path('dashbordTable/delete_table/<int:tableid>',
         views.delete_table, name='delete_table'),

]
