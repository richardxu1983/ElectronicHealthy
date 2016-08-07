function getCookie(name){
    var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return x ? x[1]:undefined;
}

$(document).ready(function(){
    $("#login").click(function(){
        var user = $("#username").val();
        var pwd = $("#password").val();
        var hash_value = calcMD5(user + pwd);
        var pd = {"username":user, "hash_value":hash_value, "_xsrf":getCookie("_xsrf")};
        $.ajax({
            type:"post",
            url:"/",
            data:pd,
            cache:false,
            success:function(data){
                if(data.status_code == "-2"){
                    alert("账号已经被冻结,请联系管理员!")
                }else if(data.status_code == "-1"){
                    alert("用户名或密码错误,请重新输入!")
                }else if(data.status_code == "-3"){
                    alert("用户名或密码为空,请重新输入!")
                }else {
                    window.location.href = "/index";
                }
            },
            error:function(){
                alert("error!");
            },
        });
    });
});