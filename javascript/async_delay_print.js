/*jshint esversion: 6 */ 

// Code here will be linted with JSHint.
/* jshint ignore:start */
async function timeout(ms) {
    await new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

async function asyncPrint(value, ms) {
    await timeout(ms);
    console.log(value);
}
// Code here will be ignored by JSHint.
/* jshint ignore:end */

asyncPrint('hello world', 5000);