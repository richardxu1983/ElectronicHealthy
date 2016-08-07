function getCookie(name){
    var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return x ? x[1]:undefined;
}

$(document).ready(function(){
    $("#logout").click(function(){
        var pd = {"_xsrf":getCookie("_xsrf")};
        $.ajax({
            type:"post",
            url:"/userManage",
            data:pd,
            cache:false,
            success:function(data){
                window.location.href = "/";
            },
            error:function(){
                alert("error!");
            },
        });
    });
});