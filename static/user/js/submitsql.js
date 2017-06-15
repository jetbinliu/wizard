$("#btn-submitsql").click(function (){
	//获取form对象，判断输入，通过则提交
	var formSubmit = $("#form-submitsql");

	if (validateForm(formSubmit)) {
		formSubmit.submit();
	}
});


function validateForm(element) {
	var result = true;
	element.find('[required]').each(
		function () {
			var fieldElement = $(this);
			//如果为null则设置为''
			var value = fieldElement.val() || '';
			if (value) {
				value = value.trim();
			}
			if (!value || value === fieldElement.attr('data-placeholder')) {
				alert((fieldElement.attr('data-name') || this.name) + "不能为空!!！");
				// $('#alert-modal-body').html(data.msg);
				// $('#alert-modal').modal({
				// 	keyboard: true
				// });
				result = false;
				return result;
			}
		}
	);
	return result;
}

$(document).ready(function () {
	// 定义一个空数组
	var sub_review_mans = [];
	// $('input[id^="sub_review_man_"]').each(function () {
	// 获取所有审核人, 并存入数组
	$("input.sub_review_man").each(function () {
		sub_review_mans.push($(this).val());
	});

	$("#review_man").change(function () {
		var review_man = $(this).val();
		alert(review_man)
	});
});



// $("#review_man").change(function () {
//     var review_man = $(this).val();
//
//     console.log(review_man);
//     $("#sub_review_man_" + review_man).hide();
//
// 		if ($(this).val() != review_man) {
// 			$(this).show();
// 		}
//     });
// });
//
// $(".sub_review_man").change(function () {
// 	var sub_review_man = $(this).val();
// 	alert(sub_review_man);
// 	$("select[name=review_man] option").each(function () {
// 		if ($(this).val() == "is-empty" || $(this).val() == sub_review_man) {
// 			$(this).attr("disabled", "");
// 		} else {console.log($(this).val());}
// 	});
// });


