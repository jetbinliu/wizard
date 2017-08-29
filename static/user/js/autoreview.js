$("#btn-autoreview").click(function(){
	//先做表单验证，成功了提交ajax给后端
	if (validate()) {
		autoreview();
	}
});


function validate() {
	var result = true;
	var clusterName = $("#cluster_name").val();
	var sqlContent = $("#sql_content").val();
	if (sqlContent === null || sqlContent.trim() === "" || sqlContent == $("#sql_content").attr("placeholder")) {
		var msgbox = "SQL内容不能为空！";
		$('#alert-modal-body').html(msgbox);
		$('#alert-modal').modal({
			keyboard: true
		});
		return result = false;
	} else if (clusterName === null || clusterName == $("#cluster_name").attr("data-placeholder")) {
		var msgbox = "请选择要上线的集群！";
		$('#alert-modal-body').html(msgbox);
		$('#alert-modal').modal({
			keyboard: true
		});
		return result = false;
	}
	return result;
}


function autoreview() {
	var clusterName = $("#cluster_name").val();
	var clusterDB = $("#cluster_db").val();
	var sqlContent = $("#sql_content").val();

	sqlContent =  'use ' + clusterDB + ';\n' + sqlContent;
	
	//将数据通过ajax提交给后端进行检查
	$.ajax({
		type: "post",
		url: "/sqlreview/simplecheck/",
		dataType: "json",
		data: {
			sql_content: sqlContent,
			cluster_name: clusterName
		},
		complete: function() {

		},
		success: function (data) {
			if (data.status == 0) {
				var result = data.data;
				var finalHtml = "";
				for (var i=0; i<result.length; i++) {
					//索引5是SQL，4是审核建议
					var sql = result[i][5].replace(/\n/g,'<br>');
					var suggest = result[i][4].replace(/\n/g,'<br>');
					alertStyle = "alert-success";
					if (result[i][4] != "None") {
						alertStyle = "alert-danger";
					}
					finalHtml += "<div class='alert alert-dismissable " + alertStyle + "'> <button type='button' class='close' data-dismiss='alert' aria-hidden='true'>x</button> " +
						"<table class=''> <tr> <td valign='top' width='600px'><strong>SQL语句：</strong><br/>" + sql + "</td> <td valign='top'><strong>自动审核结果：</strong><br/>" + suggest + "</td> </tr> </table> </div>";
				}

				$("#inception-result-col").html(finalHtml);
				//填充内容后展现出来
				$("#inception-result").show();
			} else {
                // alert("status: " + data.status + "\nmsg: " + data.msg + data.data);
                var msgbox = "status: " + data.status + "<br/>msg: " + data.msg + data.data
                $('#alert-modal-body').html(msgbox);
                $('#alert-modal').modal({
        			keyboard: true
                });
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert(errorThrown);
		}
	});	

}
