$(document).ready(function (){
    // 执行按钮点击状态变化
    $("#btnExecute").click(function(){
        $(this).button('loading').delay(2000).queue(function() {
            $(this).button('reset');
            $(this).dequeue();
        });
    });

    // 如果正在执行修改动作的当前登录用户，不是发起人，则异常.
    $("#reject_modification").click(function () {
        var loginUser = $("#loginUser").text().split('(')[0];
        var engineer = $("#id_engineer").text();
        if (loginUser != engineer) {
            $(this).attr('href', '#');
            var msgbox = '当前登录用户不是发起人，请重新登录.';
            $('#alert-modal-body').html(msgbox);
            $('#alert-modal').modal({
                keyboard: true
            });
        }
    });

    // 撤回工单小提示
    $("#btnCancel").tooltip({html : true });

    var status = $("#workflowDetail_status").text();
    if (status=="等待审核人审核"){
    setInterval("startRequest()",1000);
  }
});



function startRequest()
{
    $("#date").text((new Date()).toString());
    var workflowid = $("#workflowDetail_id").val();
    var sqls = sqlStrings();

    for(var i = 0; i < sqls.length; i++){
        var j = i + 1
        sql = sqls[i];
        $.ajax({
            type: "post",
            url: "/getOscPercent/",
            dataType: "json",
            data: {
                workflowid: workflowid,
                sqlString: sql,
            },
            complete: function () {
            },
            success: function (data) {
                if (data.status == 0) {
                    pct = data.data.percent;
                    $("div#sql_" + j).attr("style", "width: " + pct + "%");
                }
            },
            error: function () {
            }
        });
        }
}

function sqlStrings() {
    var sqls = new Array();
    $(".sqlString").each(function(){
      sqls.push($(this).text());
    });
    return sqls;
}
