#!/usr/bin/env node
const program = require('commander');   //npm i cmander -D

program.version('1.0.0')
    .usage('<command> [项目名称]')
    .command('hello', 'hello')
    .parse(process.argv);