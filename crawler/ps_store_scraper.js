function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

function getPageQuantity() {
    let quantity = document.querySelectorAll('.psw-button.psw-b-0.psw-page-button.psw-p-x-3.psw-r-pill.psw-l-line-center.psw-l-inline.psw-t-size-3.psw-t-align-c:last-of-type');
    quantity = quantity[quantity.length - 1].querySelector('.psw-fill-x ').textContent;
    return parseInt(quantity);
}

function scrollToBottom() {
    return new Promise((resolve => {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
        setTimeout(resolve, 1000);
    }))
}

function downloadJson(json, name) {
    let blob = new Blob([json], { type: 'application/json' });
    let link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name;
    link.click();
}

//獲得遊戲名稱、網址、圖片
async function gameInfo() {
    await sleep(Math.random() * 1000 + 1500);
    let pageQuantity = getPageQuantity();
    console.log("開始爬蟲共有：", pageQuantity, "頁");

    for (let page = 1; page <= pageQuantity; page++) {
        await sleep(5000);
        await scrollToBottom();
        await sleep(2500);
        let gameElement = document.querySelectorAll('.psw-grid-list.psw-l-grid > li');
        let nextPageButton = document.querySelector('button[aria-label="前往下一頁"]');
        for (let item = 0; item < gameElement.length; item++) {
            let gameImage = gameElement[item].querySelector('.psw-fade-in.psw-top-left.psw-l-fit-cover').getAttribute('src');
            let gameName = gameElement[item].querySelector('.psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2').textContent;
            let gameLink = 'https://store.playstation.com' + gameElement[item].querySelector('.psw-link.psw-content-link').getAttribute('href');
            let itemInfo = {
                name: gameName,
                img: gameImage,
                url: gameLink
            };
            itemsInfo.push(JSON.stringify(itemInfo));
        }
        nextPageButton.click();
    }
    console.log('Json資料：' + itemsInfo);
    downloadJson(itemsInfo, './raw_data/playstation_itemsInfo.json');
}

async function main() {
    await sleep(Math.random() * 1000 + 1500);
    const axios = require('axios');
    const cheerio = require('cheerio');
    const fs = require('fs');
    const gameInfo = require('./raw_data/playstation_itemsInfo.json');
    for (let item = 0; item < gameInfo.length; item++) {
        console.log(item + '/' + gameInfo.length);
        await sleep(Math.random() * 1000 + 1500);
        let response = await axios.get(gameInfo[item].url);
        const $ = cheerio.load(response.data);
        let gameName = $('.psw-m-b-5').text();
        let gameRating = $('.psw-t-subtitle.psw-t-bold.psw-l-line-center').text();
        let gamePrice = $('.psw-t-title-m.psw-m-r-4:first').text();
        let gamePlatform = $('[data-qa="gameInfo#releaseInformation#platform-value"]').text().split(',');
        let gameDate = $('[data-qa="gameInfo#releaseInformation#releaseDate-value"]').text();
        let gamePublisher = $('[data-qa="gameInfo#releaseInformation#publisher-value"]').text();
        let gameCategory = $('[data-qa="gameInfo#releaseInformation#genre-value"]').text().split(',');
        let itemInfo = {
            name: gameName,
            img: gameInfo[item].img,
            url: gameInfo[item].url,
            rating: gameRating,
            price: gamePrice,
            platform: gamePlatform,
            date: gameDate,
            publisher: gamePublisher,
            category: gameCategory
        };
        itemsInfo.push(itemInfo);
    }
    fs.writeFileSync('./raw_data/playstation_gameInfo.json', JSON.stringify(itemsInfo));
}

// const fetch = require('node-fetch');
var itemsInfo = [];
main()