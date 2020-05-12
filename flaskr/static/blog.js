require([
    'dojo/dom',
    'dojo/dom-class',
    'dojo/dom-attr',
    'dojo/dom-construct',
    'dojo/query',
    'dojo/request/xhr',
    'dojo/ready'
], function (dom,domClass,domAttr,domConstruct,query,xhr,ready) {
    ready(function () {

        query('.edit-message').on('click',function () {
            console.log(this.dataset.id);

            xhr(this.dataset.id+'/update', {
                method: 'GET',
                handleAs: 'json'
            }).then(
                function (response) {
                    console.log(response);
                    //const form = domConstruct.create('form',{});

                    const form = '<form style="width: 70%;" method="post" action='+response.id+'/update">\n' +
                    '        <div class="form-group">\n' +
                    '            <label for="title">Title</label>\n' +
                    '            <input class="form-control" name="title" id="title" value="'+response.title+'" required>\n' +
                    '        </div>\n' +
                    '        <div class="form-group">\n' +
                    '            <label for="body">Body</label>\n' +
                    '            <textarea class="form-control" rows="10" name="body" id="body">'+response.body+'</textarea>\n' +
                    '        </div>\n' +
                    '        <div class="form-group">\n' +
                    '            <input class="btn btn-success" type="submit" value="Save">\n' +
                    '            <a class="btn btn-danger" href="{{ url_for(\'blog.delete\', id=post[\'id\']) }}" role="button">Delete</a>\n' +
                    '        </div>\n' +
                    '    </form>';

                    dom.byId('main-content').innerHTML = form;

                    //dom.byId('main-content').innerHTML = response;

                },
                function (err) {
                    console.log(err);
                });

            // xhr(this.dataset.id+'/update', {
            //     method: 'GET',
            //     handleAs: 'text'
            // }).then(
            //     function (response) {
            //         console.log(response);
            //         dom.byId('main-content').innerHTML = response;
            //     },
            //     function (err) {
            //         console.log(err);
            //     });

        });
    });
});