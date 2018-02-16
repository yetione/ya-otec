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
        console.log('changed');
        $toggleBtn.data('state', state);
        if (state){
            $toggleBtn.removeClass('btn-success').addClass('btn-danger').text('Stop');
        }else{
            $toggleBtn.removeClass('btn-danger').addClass('btn-success').text('Start');
        }

    });
    $(document).on('spiderVisitedLinkAdd', function(event, link){
        var $newRow = $('<tr style="opacity: 0"><td>'+link.url+'</td></tr>');
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
    //table.startUpdater();

    /*
    setInterval(function(){
        spider.get_data(function(d){
            if (d.length){
                var $element = $('<tr style="opacity: 0"><td>'+decodeURI(d[0].url)+'</td></tr>');
                $('#shumHistory > table > tbody').prepend($element);
                $element.stop().animate({opacity:1}, 500)
            }

        })
    }, 2);
    */

    $('#stopSpiderBtn').on('click', function(event){
        spider.stop(function (state) {
            console.log('spider stopped')
        });
    });

    $('#startSpiderBtn').on('click', function(event){
        spider.start(function (state) {
            console.log('spider started')
        });
    });
});

