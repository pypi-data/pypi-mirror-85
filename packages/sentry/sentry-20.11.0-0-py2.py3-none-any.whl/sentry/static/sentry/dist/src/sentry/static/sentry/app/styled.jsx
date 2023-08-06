/* HACK(BYK): This file is a slightly modified backport of
 *
 * !!! DELETE ME WHEN UPGRADING TO EMOTION@11 !!!
 *
 * https://github.com/emotion-js/emotion/pull/1501 and
 * https://github.com/emotion-js/emotion/pull/1664 to
 * fix our TypeScript compile times and memory usage as
 * emotion@10 is known to generate too many new types due
 * to improper use of generics.
 *
 * This is especially pronounced with TS 3.7+
 * See https://github.com/microsoft/TypeScript/issues/24435
 * See https://github.com/microsoft/TypeScript/issues/34920
 */
import styled from '@original-emotion/styled';
export default styled;
//# sourceMappingURL=styled.jsx.map