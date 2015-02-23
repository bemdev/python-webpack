var path = require('path');

module.exports = {
    context: path.join(__dirname, 'test_bundle'),
    entry: './entry.js',
    output: {
        path: path.join(__dirname, 'static_root', 'bundles'),
        filename: 'bundle-[hash].js'
    }
};