function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
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
    const axios = require('axios');
    const cheerio = require('cheerio');
    const fs = require('fs');
    console.log("開始爬蟲共有：", 41, "頁");
    let itemsInfo = [];
    for (let page = 1; page <= 41; page++) {
        console.log(page + '/' + 41);
        await sleep(Math.random() * 1000 + 1500);
        let response = await axios.get('https://store.nintendo.com.hk/games/all-released-games?p=' + page);
        const $ = cheerio.load(response.data);
        $('.category-product-item').each(function (index) {
            let gameImage = $(this).find('img').attr('data-src');
            let gameName = $(this).find('.category-product-item-title-link').text().trim();
            let gameLink = $(this).find('.category-product-item-title-link').attr('href');
            let itemInfo = {
                name: gameName,
                img: gameImage,
                url: gameLink
            }
            itemsInfo.push(itemInfo);
        })
    }
    fs.writeFileSync('./raw_data/nintendo_itemsInfo.json', JSON.stringify(itemsInfo));
}

async function main() {
    await sleep(Math.random() * 1000 + 1500);
    const axios = require('axios');
    const cheerio = require('cheerio');
    const fs = require('fs');
    const gameInfo = require('./raw_data/nintendo_itemsInfo.json');
    for (let item = 0; item < gameInfo.length; item++) {
        console.log(item + '/' + gameInfo.length);
        await sleep(Math.random() * 1000 + 1500);
        let response = await axios.get(gameInfo[item].url);
        const $ = cheerio.load(response.data);
        let gameName = $('.page-title').text().replace('\n', '').trim();
        let gameRating = 0;
        let gamePrice = $('.price:first').text().replace('HKD ', '') * 4.03;
        let gamePlatform = $('.product-attribute.platform').find('.product-attribute-val').text().split(',');
        let gameDate = $('.product-attribute.release_date').find('.product-attribute-val').text();
        let gamePublisher = $('.product-attribute.publisher').find('.product-attribute-val').text();
        let gameCategory = $('.product-attribute.game_category').find('.product-attribute-val').text().split(',');
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
        // console.log(itemInfo);
        itemsInfo.push(itemInfo);
    }
    fs.writeFileSync('./raw_data/nintendo_gameInfo.json', JSON.stringify(itemsInfo));
}

var itemsInfo = [];
main()