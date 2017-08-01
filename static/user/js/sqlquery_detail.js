/**
 * Created by Kevin on 2017/7/21.
 */
$(document).ready(function () {
    // 鼠标移动到脱敏字段上方时现实原始信息
    var encrypted_td = "";
    $("td.sensitive_fields").hover(
        function () {
            encrypted_td = $(this)
            var encrypted_field = encrypted_td.text();
            sessionStorage.setItem("encrypted_field", encrypted_field);
            if (encrypted_field.substr(0,14) == "pbkdf2_sha256$") {
                $.ajax({
                    url: "/sqlquery/desensitization/",
                    type: "post",
                    data: {"encrypted_field": encrypted_field},
                    dataType: "json",
                    async: true,
                    complete: function () {
                    },
                    success: function (data) {
                        console.log(data.data);
                        encrypted_td.html('<font color="red">' + data.data + '</font>');
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        alert(errorThrown);
                    }
                });
            }
        },
        function () {
            encrypted_td.text(sessionStorage.getItem("encrypted_field"));
        }
    );
});
