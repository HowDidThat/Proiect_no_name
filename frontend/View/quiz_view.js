class widged{
    add(component) {}
    remove(component) {}
    display() {}
    refresh(){}
}

class Card extends widget(){
    question;
    diseases;
    symptoms;
    
    addDesease(){}
    addSymptom(){}
}


class Question extends widged{
    constructor(name, text) {
        super();
        this.name = name;
        this.text = text;
    }
    animate(){}    
}

class DiseaseEntry extends widget{
    constructor(name, text) {
        super();
        this.name = name;
        this.text = text;
    }
    check(){}
    uncheck(){}
    ruleOut(){}
}

class SymptomEntry extends widget{
    constructor(name, text) {
        super();
        this.name = name;
        this.text = text;
    }
    check(){}
    uncheck(){}
    ruleOut(){}
}


class quizView{
    constructor(){}
    createQuizInfoWidget(){}
    createQuestionInfoWidget(){}
    addCard(){}
}