
class TextObject {
    constructor(text) {
        if (text === undefined || text === null) {
            this.text = "";
        }
        else
        {
            this.text = text;
        }

        this.compiled = "";
        this.statuses = [];
        this.type = "input";
    }

    get getText() {
        return this.text;
    }

    get getCompiled() {
        return this.compiled;
    }

    get getStatuses() {
        return this.statuses;
    }


    setText(text) {
        this.text = text;
        this.compile(this.text);
    }

    compile(text) {
        this.compiled = text;
    }

}

class RegexObject {
    constructor(text) {
        this.text = text;
        this.type="span"
    }
}

class WildcardObject extends RegexObject {
    constructor() {
        super("...")
        this.compiled = ".*";
        this.statuses = [];
    }
}

class OrObject extends RegexObject{
    constructor() {
        super("OR")
        this.compiled = "|";
    }

}

class DictionaryObject {
    constructor(dictionary_name) {
        this.text = "{" + dictionary_name + "}"
        this.compiled = "dict:'\\(" + dictionary_name + "\\)'" 
        this.statuses = [];
        this.type = "span";
    }

}
const classesMapping = {
    'TextObject': TextObject,
    'WildcardObject': WildcardObject,
    'OrObject': OrObject,
    'DictionaryObject': DictionaryObject
}