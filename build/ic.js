"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const process_1 = require("process");
const endp = "https://smartasset.com/taxes/income-taxes?render=json"; // API endpoint
const enc_str = "ud-it-household-income=120000&ud-current-location=ZIP|14602"; // data
function main() {
    const data = argParse();
}
function argParse() {
    const args = process.argv.slice(2);
    // do stuff with args
    // ...
    const data = [0.8, null, 10800, 112000.0, [70000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 120000]];
    for (const [i, a] of args.entries()) {
        if (a === "-h" || a === "--help") {
            console.log("Usage:\n" +
                "$ node ic.js [-s] [-z] [-i] [-r] [-d]\n" +
                "-s \tpercentage of annual salary dedicated to savings\n\tFORMAT: 0.5 or 0.75 (any decimal %)\n\n" +
                "-z \tzipcode override\n\n" +
                "-i \tcomma-separated list of incomes to include\n\tFORMAT: 1,2,3,4 (comma-separated, no spaces, just integers)\n\n" +
                "-r \tmonthly rent\n\n" +
                "-d \ttotal (college) debt (adding estimated interest over time to this number in advance would be ideal)");
            process_1.exit(0);
        }
        else if (a === "-s") {
            data[0] = parseFloat(args[i + 1]);
        }
        else if (a === "-z") {
            data[1] = args[i + 1];
        }
        else if (a === "-r") {
            data[2] = parseInt(args[i + 1]);
        }
        else if (a === "-d") {
            data[3] = parseFloat(args[i + 1]);
        }
        else if (a === "-i") {
            const inc = args[i + 1].split(",");
        }
    }
    return data;
}
function moveLater() {
    axios_1.default({
        method: "post",
        url: endp,
        data: enc_str,
        headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
    }).then((response) => {
        var res = response.data;
        console.log(res['user_data']['ud-it-household-income']['value']);
        console.log(res['page_data']['2020']['totalEffectiveTaxRate']);
    }, error => {
        console.log(error);
    });
}
if (require.main === module) {
    main();
}
