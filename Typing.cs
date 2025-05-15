using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using System;
using System.Linq;
using WindowsInput;
using System.Threading;

class Program
{
    static void Main(string[] args)
    {
        // WebDriver Chrome
        var options = new ChromeOptions();
        //options.AddArgument("--headless=new");
        // adding argument to disable the AutomationControlled flag 
        options.AddArgument("--disable-blink-features=AutomationControlled");
        // exclude the collection of enable-automation switches 
        options.AddExcludedOption("enable-automation");
        // turn-off userAutomationExtension 
        options.AddAdditionalChromeOption("useAutomationExtension", false);
        options.AddArgument("--disable-extensions");
        options.AddArgument("--profile-directory=Default");
        options.AddArgument("--incognito");
        options.AddArgument("--disable-plugins-discovery");
        options.AddArgument("--start-maximized");

        using (var driver = new ChromeDriver(options))
        {
            while (true)
            {
                driver.Navigate().GoToUrl("https://humanbenchmark.com/login");

                try
                {
                    // Wait for the element to be present (up to 10 seconds)
                    var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
                    var usernameField = wait.Until(d => d.FindElement(By.XPath("//input[@name='username']")));
                    
                    // Interact with the field
                    usernameField.Click();          // Focus the field
                    usernameField.Clear();          // Clear existing text (if any)
                    usernameField.SendKeys("micpowers98@gmail.com");  // Type your username
                    
                    Console.WriteLine("Successfully entered username!");
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }

                try
                {
                    // Wait for the element to be present (up to 10 seconds)
                    var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
                    var passwordField = wait.Until(d => d.FindElement(By.XPath("//input[@name='password']")));
                    
                    // Interact with the field
                    passwordField.Click();          // Focus the field
                    passwordField.Clear();          // Clear existing text (if any)
                    passwordField.SendKeys("Idnarb10!!");  // Type your password
                    
                    Console.WriteLine("Successfully entered password!"); 
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }

                try
                {
                    // Wait for the element to be present (up to 10 seconds)
                    var loginButton = driver.FindElement(By.XPath("//input[@type='submit' and @value='Login']"));
                    loginButton.Click();
                    
                    Console.WriteLine("Successfully logged in!");    
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }

                Thread.Sleep(3000);

                try
                {
                    // Wait for the play link to be clickable
                    var playLink = driver.FindElement(By.CssSelector("a[href*='/tests/typing'] svg[data-icon='play-circle']")).FindElement(By.XPath(".."));
                    
                    Thread.Sleep(1000);
                    // Click the link
                    playLink.Click();
                    Console.WriteLine("Successfully clicked Play button");
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }

                try
                {
                    // Wait for the letters container to load
                    var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
                    var lettersContainer = wait.Until(d => d.FindElement(By.ClassName("letters")));

                    // Click the typing area to focus it
                    var typingArea = driver.FindElement(By.ClassName("letters"));
                    typingArea.Click();
                    
                    // Extract all character spans
                    var characterSpans = lettersContainer.FindElements(By.TagName("span"));
                    
                    // Create a list of characters (including spaces and punctuation)
                    var characters = characterSpans.Select(span => span.Text.Length > 0 ? span.Text : " ").ToArray();
                    
                    // Type the characters using WindowsInput
                    var inputSimulator = new InputSimulator();
                    inputSimulator.Keyboard.TextEntry(string.Join("", characters));
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                }

                bool save = false;
                try
                {
                    // Wait for the WPM element to load
                    var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
                    var wpmElement = wait.Until(d => d.FindElement(By.CssSelector("h1.css-0")));
                    
                    // Extract the text (e.g., "15553wpm")
                    var wpmText = wpmElement.Text;
                    
                    // Extract only the numeric part
                    var wpmNumberStr = new string(wpmText.Where(char.IsDigit).ToArray());
                    if (int.TryParse(wpmNumberStr, out int wpmNumber))
                    {
                        if (wpmNumber >= 25000)
                        {
                            save = true;
                        }
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }
                
                try
                {
                    // Wait for button to be clickable (up to 10 seconds)
                    var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
                    var saveButton = wait.Until(d => d.FindElement(By.CssSelector("button.css-qm6rs9")));
                    
                    // Click the button
                    if (save)
                    {
                        saveButton.Click();
                        Console.WriteLine("Successfully clicked 'Save score'");
                    }
                    else
                    {
                        Console.WriteLine("Score too low.");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }
            }
        }
    }
}