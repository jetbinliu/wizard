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
			if (! value || value === fieldElement.attr('data-placeholder')) {
				var msgbox = (fieldElement.attr('data-name') || this.name) + "不能为空!!!";
				$('#alert-modal-body').html(msgbox);
				$('#alert-modal').modal({
					keyboard: true
				});
				result = false;
				return result;
			}
		}
	);
	return result;
}

$(document).ready(function () {
	// 定义一个空数组
	var review_mans = [];
	// $('input[id^="sub_review_man_"]').each(function () {
	// 遍历获.sub_review_man取所有审核人, 并存入数组
	$(".sub_review_man").each(function () {
		review_mans.push($(this).val());
	});

	// 选中主审核人，则在副审核人里把他隐藏
	$("#review_man").change(function () {
		var review_man = $(this).val();
		$.each(review_mans, function (index,value) {
			if (value == review_man) {
				$("#sub_review_man_" + value).hide(1000);
			} else {
				$("#sub_review_man_" + value).show(1000);
			}
        });
	});

	// 点击“添加副审核人”时判断，如果还未选择主审核人则：修改折叠窗属性使不能打开并弹窗提示
	$("#add_sub_review_man").click(function () {
		var reviewMan = $("#review_man").val();
		if (reviewMan == null) {
			$("#collapse_sub_review_man").attr('class', "panel-collapse collapse in");
			var msgbox = "请务必选择主审核人！";
			$('#alert-modal-body').html(msgbox);
			$('#alert-modal').modal({
				keyboard: true
			});
		}
    });

	// 鼠标离开副审核人区域后就折叠起来
	$("#collapse_sub_review_man").hover(function () {},
	function () {
		$(this).attr('class', "panel-collapse collapse");
    });
});

