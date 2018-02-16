new QWebChannel(qt.webChannelTransport, function(channel) {
    window.bridge = channel.objects.bridge;
    //window.spider = channel.objects.spider;
    window.spider = new Spider(channel.objects.spider);


    /*spider.task_done.connect(function(task){
        console.log('task done ' + task.url)
    });*/
    /*spider.get_state(function (state) {
        console.log('spider state ' + (state ? 'active' : 'disable'))
    });*/
    /*spider.state_changed.connect(function(state){
        console.log('spider change state ' + (state ? 'active' : 'disable'))
    });
    */
    // bridge.print('Hello world!');
    // channel.objects.bridge.print('TEST')
});
var table = new Spider('#shumHistory');

$(document).ready(function(){
    var $toggleBtn = $('#toggleSpider');
    $(document).on('spiderStateChange', function(event, state){
        $toggleBtn.data('state', state);
        if (state){
            $toggleBtn.removeClass('btn-success').addClass('btn-danger').text('Stop');
        }else{
            $toggleBtn.removeClass('btn-danger').addClass('btn-success').text('Start');
        }

    });
    $(document).on('spiderVisitedLinkAdd', function(event, link){
        var $newRow = $('<tr style="opacity: 0" data-toggle="modal" data-target="#urlDetailModal" class="visited-link"><td>'+link.url+'</td></tr>');
        $newRow.data('full', link);
        $('.j-visited-links > tbody').prepend($newRow);
        $newRow.stop().animate({opacity:1}, 500);
    });

    $toggleBtn.on('click', function (event) {
        var state = $toggleBtn.data('state');
        $toggleBtn.prop('disabled', true);
        if (state){
            spider.stop(function(){
                $toggleBtn.prop('disabled', false);
            });
        }else{
            spider.start(function(){
                $toggleBtn.prop('disabled', false);
            });
        }
    });

    $('#historyModal').on('show.bs.modal', function (event) {
        bridge.get_urls(20, function(result){
            var html = '';
            for (var i=0;i<result.length;++i){
                html += ' <tr>' +
                    '<th scope="row">'+(i+1)+'</th>' +
                    '<td>'+(result[i].url)+'</td>' +
                    '<td><button type="button" class="btn btn-outline-success btn-sm" data-toggle="modal" data-target="#historyElementModal">Edit</button></td>'+
                    '</tr>';
            }
            $('#url-table>tbody').html(html);
        });
    });

    $('#urlDetailModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var url = button.data('full');
        var modal = $(this);
        modal.find('.j-url-url>td').html('<a href="'+url.url+'">'+url.url+'</a>');
        modal.find('.j-url-code>td').text(url.result_code);
        modal.find('.j-url-time>td').text(url.request_time);
        modal.find('.j-url-size>td').text(url.page_size);
        modal.find('.j-url-ip>td').text(url.host_ip);

    });
});

