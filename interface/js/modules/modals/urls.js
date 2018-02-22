import $ from  "jquery";

export default class UrlsModal{

    constructor($element){
        this.$element = $element;

        this.$listTab = this.$element.find('.list-tab');
        this.$loadMoreBtn = this.$listTab.find('.j-load-more');
        this.$listTable = this.$listTab.find('.j-list-table');

        this.$elementTab = this.$element.find('.element-tab');
        this.$urlId = this.$elementTab.find('#element-id');
        this.$urlAddress = this.$elementTab.find('#element-address');
        this.$urlHeaders = this.$elementTab.find('#element-headers');
        this.$urlCookies = this.$elementTab.find('#element-cookie');
        this.$urlDateAdd = this.$elementTab.find('#element-date-add');
        this.$urlLastVisit = this.$elementTab.find('#element-last-visit');
        this.$urlRequestType = this.$elementTab.find('#element-request-type');
        this.$urlIsActive = this.$elementTab.find('#element-is-active');
        this.$urlAddBy = this.$elementTab.find('#element-add-by');

        this.itemsPerPage = 10;
        this.page = 1;
        this.cleanElementTab();
        this.bindEvents();
    }

    bindEvents() {
        let self = this;
        this.$element.on('show.bs.modal', function(event) {
            let initBtn = $(event.relatedTarget);
            self.$elementTab.hide();
            self.$listTab.show();
            self.loadNextPage();
            self.$loadMoreBtn.off('click._modal').on('click._modal', function () {
                self.page++;
                self.loadNextPage();
            });
        });
    }

    cleanListTable() {
        this.$listTable.find('tbody').html('');
    }

    cleanElementTab() {
        this.$urlId.val('');
        this.$urlId.parent().show();

        this.$urlAddress.val('');
        this.$urlAddress.parent().show();

        this.$urlHeaders.val('');
        this.$urlHeaders.parent().show();

        this.$urlCookies.val('');
        this.$urlCookies.parent().show();

        this.$urlDateAdd.val('');
        this.$urlDateAdd.parent().show();

        this.$urlLastVisit.val('');
        this.$urlLastVisit.parent().show();

        this.$urlRequestType.val('');
        this.$urlRequestType.parent().show();

        this.$urlIsActive.val(0);
        this.$urlIsActive.parent().show();

        this.$urlAddBy.val('');
        this.$urlAddBy.parent().show();
    }

    setElementTabData(data) {
        if ('id' in data){this.$urlId.val(data.id);} else {this.$urlId.hide();}
        if ('address' in data){this.$urlAddress.val(data.address);} else {this.$urlAddress.hide();}
        if ('headers' in data){
            let i = 0;
            for (let name in data.headers){
                let template = this.$urlHeaders.find('.header-row.original').clone();
                if (i !== 0){
                    template.removeClass('original');
                }
                template.insertAfter(this.$urlHeaders.find('.header-row:last-child'));
                template.find('.header-name').val(name);
                template.find('.header-value').val(data.headers[name]);
                i++;
            }
            this.$urlHeaders.find('.header-row.original:first-child').remove();
            //this.$urlHeaders.val(data.headers);
        } else {
            this.$urlHeaders.hide();
        }
        if ('cookies' in data){this.$urlCookies.val(data.cookies);} else {this.$urlCookies.hide();}
        if ('date_add' in data){this.$urlDateAdd.val(data.date_add);} else {this.$urlDateAdd.hide();}
        if ('last_visit' in data){this.$urlLastVisit.val(data.last_visit);} else {this.$urlLastVisit.hide();}
        if ('request_type' in data){this.$urlRequestType.val(data.request_type);} else {this.$urlRequestType.hide();}
        if ('is_active' in data){this.$urlIsActive.val(data.is_active);} else {this.$urlIsActive.hide();}
        if ('add_by' in data){this.$urlAddBy.val(data.add_by);} else {this.$urlAddBy.hide();}
    }

    loadNextPage() {
        let self = this;
        let offset = (self.page - 1) * self.itemsPerPage;
        urls.get_list({
            limit:{
                count: self.itemsPerPage,
                offset: offset
            }
        }, function(result) {
            if (result.length > 0){
                let html = '';
                for (let i=0;i<result.length;++i){
                    html += ' <tr>' +
                        '<th scope="row" class="number">'+((self.page-1)*self.itemsPerPage+i+1)+'</th>' +
                        '<td class="url">'+decodeURI(result[i].address)+'</td>' +
                        '<td class="actions"><button type="button" class="btn btn-outline-success btn-sm j-edit-url" data-url-id="'+result[i].id+'">Edit</button></td>'+
                        '</tr>';
                }
                self.$listTable.find('tbody').append(html);
                self.$loadMoreBtn.prop('disabled', false);
                self.$listTable
                    .find('.j-edit-url')
                    .off('click._edit_modal')
                    .on('click._edit_modal', function(event){
                    let entityId = $(event.target).data('url-id');
                    urls.get_by_id(entityId, function(url) {
                        if (url.length !== 1){
                            alert('Error');
                            return false;
                        }
                        url = url[0];
                        self.setElementTabData(url);
                        self.$listTab.hide();
                        self.$elementTab.show();


                    });
                })
            } else {
                self.$loadMoreBtn.prop('disabled', true);
            }
        });
    }

    loadUrls(offset, count){

    }
}