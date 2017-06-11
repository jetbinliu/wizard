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


function error(data){
	alert('something is error!');
}
//用来请求网页显示在固定位置
//　flag: 是否时左侧的主菜单
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
        success: success,
        error:error,
        dataType: 'html',
        async:false
    });
    return false;
}

//处理刷新页面，json字符串包含statusCode，url，message信息
function httpRedirect(data){
	var statusCode = data.statusCode;
	var url = data.url;
	var message = data.message;
	if (statusCode == 200){
		httpRedirectAjax(url);
	}
    alert(message);
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
		success:httpRedirect,
		error: error,
		dataType: 'json',
		async:false
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
		async:false
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
		async:false
	});
	return false;
}
function validateerror(){
	alert('validateCallback is error!');
}
//处理form表单,返回一个json字符串给httpRedirect函数进行重定向
function validateCallback(form){
	//校验失败，直接返回
	if(!$(form).valid()){
		alert("表单校验失败，无法提交!");
		return false;
	}
	var url = $(form).attr("action");
	jQuery.ajax({
		type: 'POST',
		url: url,
		data:$(form).serializeArray(),
		success: httpRedirect,
		error:validateerror,
		dataType: 'json',
		async:false
	});
	return false;
}
