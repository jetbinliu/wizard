/**
 * Created by Kevin on 2017/7/18.
 */
$(document).ready(function () {
    $("#cluster_name").change(function () {
        var cluster_info = $(this).find("option:selected").text();
        var cluster_dbs = cluster_info.split(/[:)]/)[1].split(",");
        var html = "";
        for (var i=0;i<cluster_dbs.length;i++) {
            html += '<label class="checkbox" style="font-weight: normal"><input type="radio" name="cluster_db" value="' + cluster_dbs[i].replace(/^\s\s*/, '').replace(/\s\s*$/, '') + '" required/>' + cluster_dbs[i] + '</label>'
        }
        $(".panel-body").hide();
        $(".panel-body").html(html);
        $(".panel-body").fadeIn();
   });
});