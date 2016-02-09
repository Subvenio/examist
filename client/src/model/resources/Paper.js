import { omit } from "lodash/object";
import { Resource } from "../../library";
import { compose } from "../../library/Selector";
import * as User from "../User";
import Module from "./Module"

const Paper = new Resource("paper", "id", {
    cleaner: paper => omit(paper, "questions")
});

/*
 * Add papers return when a user get's their modules.
 */
Paper.addProducerHandler(User.getModules, 
    ({ modules }) => modules.reduce((papers, module) => papers.concat(module.papers), []));

/*
 * Add papers when a specific module is selected
 */
Paper.addProducerHandler(Module.type, module => module.papers);

/*
 * Get a paper by module, year and period.
 */
export const getPaper = Paper.createStatefulResourceAction(User.selectAPI, 
    (api, module, year, period) => api.getPaper(module, year, period).then(res => res.paper));

/**
 * Select a paper based on the following criteria:
 * @param  {String}   module The module code.
 * @param  {Number}   year   The paper year.
 * @param  {String}   period The paper period.
 * @return {Function}        Selector.
 */
export const selectPaper = ({ module, year, period }) => {
    return Paper.select(papers => papers.find(paper => paper.module === module && paper.year === year && paper.period === period));
};

/**
 * Select questions for a paper.
 * @param  {Number}   paper Paper id.
 * @return {Function}       Selector.
 */
export const selectQuestions = paper => state => {
    return state.resources.questions.filter(question => question.paper === paper);
};

/*
 * Select a paper including questions. See `selectPaper` for params.
 */
export const selectPaperWithQuestions = compose(selectPaper, paper => state => ({
    ...paper,
    questions: selectQuestions(paper.id)(state)
}));

/**
 * Select a module's papers by id.
 * @param  {Number}    id Module id.
 * @return {Function}     Selector.
 */
export const selectByModule = Paper.selectAllByProp("module");

export default Paper;