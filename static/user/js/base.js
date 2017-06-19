/**
 * Created by root on 17-6-10.
 */
$(document).ready(function () {
    // 点开或者关闭主菜单时改变菜单右边"箭头"
    $(".menu").click(function () {
            /*切换折叠指示图标*/
            if ($(this).children("span:last").attr("class") == "glyphicon glyphicon-menu-left") {
                $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-down");
            } else {
                $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-left");
            }
        }
    );

    // 打开某主菜单后折叠其他主菜单
    $('.submenu').on('shown.bs.collapse', function () {
        currentId = $(this).attr('id');

        $(".submenu").each(function () {
            Id = $(this).attr('id');
            if (Id != currentId) {
                // $(this).attr("class", "submenu panel-collapse collapse");
                $(this).collapse('hide');
                // 其它菜单折叠后修改"箭头"为向左
                $(this).prev().children("span").last().attr("class", "glyphicon glyphicon-menu-left");
            }
        });
    });

    // // 鼠标移动到菜单上方时打开二级菜单
    // $(".menu").hover(
    //     function () {
    //         $(this).next().collapse('show');
    //         $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-down");
    //     },
    //     function () {
    //     }
    // );

    // 点击二级菜单后不关闭
    $(".submenu a").click(function () {
        $.cookie("navstation", $(this).html(), { path: "/" });
    });

    var navstation = $.cookie("navstation");
    if (navstation != null) {
        $(".submenu a").each(function () {
            if ($(this).html() == navstation) {
                $(this).addClass('active');
                $(this).parent().attr("class", "submenu collapse in");
                $(this).parent().prev().children("span:last").attr("class", "glyphicon glyphicon-menu-down");
            }
        });
    }
    // 点击首页后关闭侧边栏
    $(".homePage").click(function () {
        $.cookie("navstation", null, { path: "/" });
    });
});