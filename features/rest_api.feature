Feature: Rest api testing

  Scenario Outline: Get request
    Given I use GET_request to call the <endpoint>
    Then the status code should be <code>
    Examples:
      | endpoint                    | code |
      | https://icanhazdadjoke.com/ | 200  |

  Scenario Outline: Post request
    Given I use POST_request to call the <endpoint> with '<payload>'
    Then the status code should be <code>
    Examples:
      | endpoint                                  | payload                                                                 | code |
      | http://216.10.245.166/Library/Addbook.php | {"name": "My book name", "isbn": "123", "aisle": "456", "author": "Me"} | 200  |
