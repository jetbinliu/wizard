/**
 * Created by root on 17-6-14.
 */
function dig(domain){
    var url = "/dbadmin/getdomainbydig/";
    data = {"domain":domain}
    jQuery.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        async:false,
        success: dig_success
    });
}

function dig_success(data){
    $("#dig-info").html(data);
}

function clusterStatSet(cluster_type, port){
    var id = 'clusterid_' + port;
    var clusterid = document.getElementById(id).getAttribute("value");
    if(clusterid == 1){
        cluster_offline(cluster_type, port)
    }else{
        cluster_online(cluster_type, port)
    }
}

function cluster_offline(cluster_type, port){
    var url = "/dbconfig/setclusterstatus/";
    data = {"cluster_type":cluster_type,"port":port,"stat":0}
    jQuery.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        async:false,
        success: function(retdata){
            if(retdata["status"] == 0)
            {
                var id = 'clusterid_' + port;
                var clusterid = document.getElementById(id);
                clusterid.setAttribute("class", "cur_select");
                clusterid.setAttribute("class", "switchoff");
                clusterid.setAttribute("title", "点击开启");
                clusterid.setAttribute("value", "0");
            }else{
                alert("offline failed"+retdata["status"]);
            }
        },
    });

}

function cluster_online(cluster_type, port){
    var url = "/dbconfig/setclusterstatus/";
    data = {"cluster_type":cluster_type,"port":port,"stat":1}
    jQuery.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        async:false,
        success:function(retdata){
            if(retdata["status"] == 0)
            {
                var id = 'clusterid_' + port;
                var clusterid = document.getElementById(id);
                clusterid.setAttribute("class", "cur_select");
                clusterid.setAttribute("class", "switchon");
                clusterid.setAttribute("title", "点击关闭");
                clusterid.setAttribute("value", "1");
            }else{
                alert("online failed"+retdata["status"]);
            }
        },
    });
}

