/**
 * Created by ranran on 2016/7/17.
 */
 function getCookie(name) {
        var x = document.cookie.match("\\b" + name + "=([^:]*)\\b");
        return x ? x[1]:undefined;
}
$(document).ready(function () {
    $("#query_cv_cvalue_field").click(function () {
        var cv_value_field = $("#cv_value_field").val();
        var pd = {"cv_value_field":cv_value_field, "_xsrf":getCookie("_xsrf")};
        $.ajax({
            type:"post",
            url:"/queryCvvalueField", //传值
            data:pd,
            cache:false,
            success:function(data){
                if(data == "0"){
                    alter("该值域已经删除！")
                }else{
                     $("#text_area").html("自增主键:"+data[0].cvvf_inc_pk+"序号:"+data[0].cvvf_oid+"代码:"+data[0].cvvf_code);
                }

            },
            error:function () {
                alert("error!");
            },
        });
    });
});