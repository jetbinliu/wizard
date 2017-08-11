/**
 * Created by Kevin on 2017/7/18.
 */
$(document).ready(function () {
    $("#cluster_name").change(function () {
         $("#sqlquery_dbs").empty();
        var cluster_name = $(this).val();
        var html = "";
        $.ajax({
            url: "/sqlquery/getdbs/",
            type: "post",
            data: {"cluster_name": cluster_name},
            dataType: "json",
            async: true,
            complete: function () {
            },
            success: function (data) {
                $("#sqlquery_dbs").append("<ul style='margin-left: 0px;padding-left: 0px'>");
                if (data.data.length) {
                    for(var i=0; i<data.data.length; i++){
                        var db_name = data.data[i];
                        $("#sqlquery_dbs ul").append("<li class=\"sqlquery_db\" style=\"list-style-type : none\">" + '<a href="#" onclick="return fromDbGetTables_0(this);"><i class="glyphicon glyphicon-folder-close"></i>&nbsp;</a>' + "<a href=\"#\" onclick=\"return fromDbGetTables_1(this);\">" + db_name + "</a>" + "</li>");
                    }
                } else {
                    $("#cluster_db").next().html("<font color=\"red\"><b>无法获取数据库信息，请检查wizard访问集群权限。</b></font>");
                }

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
        $(".panel-body").hide();
        $(".panel-body").fadeIn();
   });
});

function fromDbGetTables_0(element) {
    var element_a = $(element)
    var element_li = element_a.parent();
    var db_name =  element_a.next().text();
    showSelectDb(db_name);
    if (element_a.children("i").attr("class") == "glyphicon glyphicon-folder-close") {
        element_a.children("i").attr("class", "glyphicon glyphicon-folder-open");
        $.ajax({
            url: "/sqlquery/gettbs/",
            type: "post",
            data: {"table_schema": db_name},
            dataType: "json",
            async: true,
            complete: function () {
            },
            success: function (data) {
                element_li.append("<ul style='margin-left: 0px;padding-left: 0px'>");
                for(var i=0; i<data.data.length; i++){
                    var tb_name = data.data[i][0];
                    var tb_comment = data.data[i][1].substr(0,6);
                    element_li.children("ul").append("<li class=\"sqlquery_tb\" style=\"list-style-type : none;margin-left: 15px\">" + "<a href=\"#\"><i class=\"glyphicon glyphicon-list-alt\"></i>&nbsp;</a>" + "<span>" + tb_name + " " + tb_comment + "</span>" + "</li>");
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    } else {
        element_a.children("i").attr("class", "glyphicon glyphicon-folder-close");
        element_li.children("ul").remove();
    }
}

function fromDbGetTables_1(element) {
    var element_a = $(element)
    var db_name =  element_a.text();
    showSelectDb(db_name);
}

function showSelectDb(db_name) {
    $("#cluster_db").val(db_name);
    $("#cluster_db").next().html("<font color=\"red\"><b>你已经选择数据库：" + db_name + "</b></font>");
}