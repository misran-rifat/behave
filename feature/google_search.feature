Feature: Google search

  Scenario Outline: User is able to search information on google
    Given user visits <url>
    Then user searches <search_word>
    Then the page title should contain the <search_word>
    Examples:
      | url                     | search_word   |
      | https://www.google.com/ | python behave |
      | https://www.google.com/ | selenium      |
      | https://www.google.com/ | spacex        |

