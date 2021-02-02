import axios from 'axios'

const url="https://smartasset.com/taxes/income-taxes?render=json";

var str = "ud-it-household-income=120000&ud-current-location=ZIP|14602";

axios({
    method: "post",
    url: url,
    data : str,
    headers : {
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
}).then((response) => {
    var res = response.data;
    console.log(res['user_data']['ud-it-household-income']['value']);
    console.log(res['page_data']['2020']['totalEffectiveTaxRate']);
}, error => {
    console.log(error);
});

