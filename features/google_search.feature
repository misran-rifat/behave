@ui
Feature: Google search

  Background: User is on Google homepage
    Given user visits https://www.google.com

  Scenario Outline: User is able to search information on google
    Then user searches <search_word>
    Then the page title should contain the <search_word>
    Examples:
      | search_word   |
      | python behave |
      | selenium      |
      | spacex        |

