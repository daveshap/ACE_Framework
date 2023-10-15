import {get} from "svelte/store";
import {currentLayerName} from "$lib/stores/configStores";

export function layerNameToBgStyle() : string
{
    switch (get(currentLayerName)) {
        case "Aspirational Layer":
            return `background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #C9A86D 0%, #FDD182 10.96%, rgba(254, 226, 175, 0.25) 35.04%, rgba(254, 235, 200, 0.06) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;`
        case "Global Strategy Layer":
            return `background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #58A19A 0%, #7CB3B5 10.96%, rgba(88, 161, 154, 0.3) 35.04%, rgba(88, 161, 154, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;`
        case "Agent Model Layer":
            return `background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #E3A2E3 0%, #E9B2E9 10.96%, rgba(227, 162, 227, 0.3) 35.04%, rgba(227, 162, 227, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;`
        case "Executive Layer":
            return `background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #A8E0E8 0%, #B2E5ED 10.96%, rgba(168, 224, 232, 0.3) 35.04%, rgba(168, 224, 232, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;`
        case "Cognitive Control Layer":
            return `background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #4AB0B9 0%, #5FBCC5 10.96%, rgba(74, 176, 185, 0.3) 35.04%, rgba(74, 176, 185, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;`
        case "Task Prosecution Layer":
            return `background: radial-gradient(123.16% 171.6% at 131.71% -14.68%, #A45534 0%, #B06642 10.96%, rgba(164, 85, 52, 0.3) 35.04%, rgba(164, 85, 52, 0.1) 48.17%, rgba(255, 255, 255, 0.00) 91.67%, rgba(255, 255, 255, 0.00) 100%);
        background-size: cover;`
        default:
            return "";
    }
}