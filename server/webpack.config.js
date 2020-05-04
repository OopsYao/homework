const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyPlugin = require('copy-webpack-plugin');
const path = require('path');
const webpack = require('webpack');

module.exports = {
    output: {
        filename: '[name].[contenthash].js'
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src/'),
            '~': path.resolve(__dirname),
            '@components': path.resolve(__dirname, './src/components'),
        }
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env", "@babel/preset-react"]
                    }
                }
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                ],
            },
            {
                test: /\.pdf$/,
                loader: 'file-loader',
                options: {
                    outputPath: 'd',
                },
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: 'public/index.html',
            base: '/'
        }),
        new CopyPlugin([
            { from: 'public' }
        ]),
        new webpack.DefinePlugin({
            DOC_TREE: JSON.stringify(require('./doc-structure')('./pdf'))
        })
    ],
    devServer: {
        historyApiFallback: true
    }
};