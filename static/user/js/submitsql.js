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


$("#review_man").change(function () {
    var review_man = $(this).val();
    $("#sub_review_man_" + review_man).hide();
});

$(".sub_review_man").change(function () {
	var sub_review_man = $(this).val();
	$("select[name=review_man] option").each(function () {
		if ($(this) == sub_review_man) {
			$(this).remove();
		}
    });

});


