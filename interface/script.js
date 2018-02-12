new QWebChannel(qt.webChannelTransport, function(channel) {
    window.bridge = channel.objects.bridge;
    window.spider = channel.objects.spider;


    /*spider.task_done.connect(function(task){
        console.log('task done ' + task.url)
    });*/
    spider.get_state(function (state) {
        console.log('spider state ' + (state ? 'active' : 'disable'))
    });
    /*spider.state_changed.connect(function(state){
        console.log('spider change state ' + (state ? 'active' : 'disable'))
    });
    */
    // bridge.print('Hello world!');
    // channel.objects.bridge.print('TEST')
});

$(document).ready(function(){
    var $toggleBtn = $('#toggleSpider');
    spider.get_state(function(state){
        $toggleBtn.data('state', state);
        if (state){
            $toggleBtn.addClass('btn-danger').text('Stop');
        }else{
            $toggleBtn.addClass('btn-success').text('Start');
        }
    });
    $toggleBtn.on('click', function (event) {
        var state = $toggleBtn.data('state');
        if (state){
            spider.stop(function(s){
                console.log('stopped');
                $toggleBtn.removeClass('btn-danger').addClass('btn-success').text('Start').data('state', s);
            });
        }else{
            spider.start(function(s){
                console.log('started');
                $toggleBtn.removeClass('btn-success').addClass('btn-danger').text('Stop').data('state', s);
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


    setInterval(function(){
        spider.get_data(function(d){
            if (d.length){
                var $element = $('<tr style="opacity: 0"><td>'+decodeURI(d[0].url)+'</td></tr>');
                $('#shumHistory > table > tbody').prepend($element);
                $element.stop().animate({opacity:1}, 500)
            }

        })
    }, 2);
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

