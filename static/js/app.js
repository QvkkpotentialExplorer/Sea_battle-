//var area = document.getElementById('area');
//var cell = document.getElementsByClassName('cell');
//let n = 5               // размер поля
//
//const User = {
//    id: 12345,
//    userShoots: 2,
//    admin: false
//}
//
////const ship = {
////    x:0,
////    y:0,
////    sStatus:false,
////    bStatus:true,
////    
////
////}
//
//
//let Admin = [12345,1236,1111]
//
//
//if (Admin.includes(User.id)){           // Изменение статуса админа
//    User.admin = true
//}
//
////if (User.admin){
////    let d = input.value()
////    User.userShoots+=d
////}                                         // добавление выстрелов
//
////if (){
////    ship.sStatus=true
////}                                         // изменение статуса корабля
//
//function generateShotMap(n) {
//    var map = [];
//    for(var yPoint=0;yPoint<n; yPoint++){
//        for(var xPoint=0;xPoint<n; xPoint++){
//            map.push({y: yPoint, x: xPoint});
//        }
//    }
//    return map
//}
////console.log(generateShotMap(n))           // создание n*n поля
//
//function getCookie(name) {
//    let matches = document.cookie.match(new RegExp(
//      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
//    ));
//    return matches ? decodeURIComponent(matches[1]) : undefined;
//  }
//
//function setCookie(name, value, options = {}) {
//
//    options = {
//      path: '/',
//    };
//  
//    if (options.expires instanceof Date) {
//      options.expires = options.expires.toUTCString();
//    }
//  
//    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
//  
//    for (let optionKey in options) {
//      updatedCookie += "; " + optionKey;
//      let optionValue = options[optionKey];
//      if (optionValue !== true) {
//        updatedCookie += "=" + optionValue;
//      }
//    }
//  
//    document.cookie = updatedCookie;
//  }
//  
//  console.log(getCookie(User))
//

