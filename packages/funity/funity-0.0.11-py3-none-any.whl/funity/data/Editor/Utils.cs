using System;
using UnityEditor;

namespace funity
{
    public static class Utils
    {
        public static void Log(string message)
        {
            Console.WriteLine($">> {message}");
        }

        public static void Quit(int returnValue, string message = null)
        {
            if (!string.IsNullOrWhiteSpace(message))
                Log(message);

            EditorApplication.Exit(returnValue);
        }

        public static void Quit(bool success, string message = null)
        {
            Quit(success ? 0 : 1, success ? "Success!" : "Failed!");
        }
    }
}