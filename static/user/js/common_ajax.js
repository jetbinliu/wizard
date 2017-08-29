/**
 * Created by root on 17-6-11.
 */

// 存储hash值和url的对应关系
hash_dict = {}

function success(data){
	//$('#content').fadeOut();
	$("#content").html(data);
	//$('#content').fadeIn();
	// docReady();
}

function cancel_success(data){
    //$('#content').fadeOut();
    $("#content").html(data);
    //$('#content').fadeIn();
    //docReady();
}


function error(XMLHttpRequest, textStatus, errorThrown){
	// alert('something is error!');
	alert(errorThrown);
}
//用来请求网页显示在固定位置
//　flag: 是否是左侧的主菜单
function executeMenu(element,flag){
    var url = $(element).attr("href");
    if(flag){
	$('ul.main-menu li.active').removeClass('active');
	$(element).parent('li').addClass('active');
	// 记录历史URL 便于回退
	$("#hide_history_url").val(url);

	var hash_value  = '#' + parseInt(Math.random()*100000);
	location.hash = hash_value;
	hash_dict[hash_value] = $("#hide_history_url").val();

	// 改变title
	//var base = $($("meta[name='base_title']")[0]).attr('content');
	//$("title").html(base + '-' + $($(element).children()[1]).html().trim());
    }

    jQuery.ajax({
        type: 'GET',
        url: url,
		dataType: 'html',
        async: true,
        success: success,
		error: error,
    });
    return false;
}

// 普通跳转normalRedirect
function normalRedirect(url='') {
	if (url == '') {
		url = sessionStorage.getItem('hide_history_url');
	}
	$(location).attr('href', url);
}

//处理刷新页面，json字符串包含statusCode，url，message信息
function httpRedirect(data){
	var statusCode = data.statusCode;
	var url = data.url;
	var message = data.message;
	if (statusCode == 200){
		httpRedirectAjax(url);
	} else {
    	// alert(message);
		$('#alert-modal-body').html(data.message);
		$('#alert-modal').modal({
			keyboard: true
		});
	}

}

//执行删除或批量删除
function executeDelete(obj,ids){
	var url = $(obj).attr("href");
	var message = $(obj).attr("title");
	if (!confirm(message))
  	{
  		return false;
  	}
	jQuery.ajax({
		type: 'POST',
		url: url,
		data:{'ids':ids},
		dataType: 'json',
		success:httpRedirect,
		error: error,
		// async:false
	});
	return false;
}
//请求url，刷新请求页面
function httpRedirectAjax(url){
    jQuery.ajax({
		type: 'GET',
		url: url,
		success: cancel_success,
		error:error,
		dataType: 'html',
		// async:false
	});
	return false;
}


// 回退到历史URL
function backHistoryURL(){
	jQuery.ajax({
		type: 'GET',
		url: $("#hide_history_url").val(),
		success: success,
		error:error,
		dataType: 'html',
		async:true,
	});
	return false;
}
function validateerror(){
	alert('validateCallback is error!');
}
//处理form表单,返回一个json字符串给httpRedirect函数进行重定向
function validateCallback(form){
	//校验失败，直接返回
	if(!$(form).validate()){
		alert("表单校验失败，无法提交!");
		return false;
	}
	var url = $(form).attr("action");
	jQuery.ajax({
		type: 'POST',
		url: url,
		dataType: 'json',
		data:$(form).serializeArray(),
		success: httpRedirect,
		error:validateerror,
		// async:false
	});
	return false;
}
