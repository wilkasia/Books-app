require([
    'dojo/_base/url',
    'dojo/dom',
    'dojo/dom-class',
    'dojo/dom-attr',
    'dojo/query',
    'dojo/ready'
], function (url,dom,domClass,domAttr,query,ready) {
    ready(function () {
        const loc = window.location.pathname;
        console.log('loc ',window.location.pathname);

        query('.vertical-menu > a').forEach(function (node) {
            if(domAttr.get(node,'href')===loc) {
                domClass.add(node,'active');
            } else {
                domClass.remove(node,'active');
            }
        });

        // query('#del-post').on('click',function () {
        //     confirm('Are you sure?');
        //
        // })
    });
});