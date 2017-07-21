/**
 * Created by Kevin on 2017/7/21.
 */
$(document).ready(function () {
    // 鼠标移动到脱敏字段上方时现实原始信息
    $("td.sensitive_fields").hover(
        function () {
            console.log($(this).text());
        },
        function () {
        }
    );
});
