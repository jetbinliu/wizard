/**
 * Created by root on 17-6-10.
 */
$(document).ready(function () {
    // 加载完毕折叠所有主菜单
    $('div[id^="collapse_"]').each(function () {
        $(this).collapse('hide');
    });

    // 点开或者关闭主菜单时改变菜单右边图标
    $(".menu").click(function () {
            /*切换折叠指示图标*/
            if ($(this).children("span:last").attr("class") == "glyphicon glyphicon-menu-down") {
                $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-up");
            } else {
                $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-down");
            }
        }
    );

    // 打开主菜单时折叠其他主菜单
    $('.submenu').on('show.bs.collapse', function () {
        currentId = $(this).attr('id');

        $(".submenu").each(function () {
            Id = $(this).attr('id');
            if (Id != currentId) {
                $(this).attr("class", "submenu panel-collapse collapse");
            }
        });
    });
});
