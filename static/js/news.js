let vm = new Vue({
    el: '#content',
    data: {
        newslists: [],
        infolist : ''
    },
    methods: {
        getnews: function () {
            $.get(
                'http://api.tianapi.com/areanews/index',
                {
                    'key': 'dfa319efc6ed6e4aa30f38804105bdfc',
                    'areaname': '湖北',
                    'num': '5'
                },
                function (data) {
                    for (let i=0;i<6;i++){
                        vm.newslists.push(data.newslist[i])
                    }
                    console.log(vm.newslists)
                }
            )
        },
        //这个ajax用来请求header的用户姓名和学号
        getname: function () {
            var id = sessionStorage.getItem('id');
            $.post(
                '/school_news/',
                {
                    'id':id
                },
                function (data) {
                    vm.infolist = data['newslist'];
                    console.log(vm.infolist)
                }
            )
        }
    },
    mounted(){
        this.getname();
        this.getnews();
    },

});
